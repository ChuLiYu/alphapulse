"""VAL-01–05: synthetic-snapshot valuation, independent of persistence and APIs."""

from dataclasses import dataclass
from datetime import date
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext

CURRENCIES = frozenset({"USD", "CAD"})
CENT = Decimal("0.01")


def _identifier(value: str) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise ValueError(
            "Identifiers must be nonempty strings of at most 128 characters"
        )


def _date(value: date) -> None:
    if type(value) is not date:
        raise ValueError("An explicit business date is required")


def _number(
    value: Decimal, maximum: str, places: int, *, positive: bool = False
) -> None:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError("Financial values must be finite Decimal instances")
    if value < 0 or (positive and value == 0) or value > Decimal(maximum):
        raise ValueError("Financial value outside the supported policy bounds")
    if value.as_tuple().exponent < -places:
        raise ValueError("Financial value exceeds the supported decimal scale")


def _currency(value: str) -> None:
    if not isinstance(value, str) or value not in CURRENCIES:
        raise ValueError("Only USD and CAD are supported")


@dataclass(frozen=True)
class Holding:
    instrument_id: str
    quantity: Decimal

    def __post_init__(self) -> None:
        _identifier(self.instrument_id)
        _number(self.quantity, "1e12", 6)


@dataclass(frozen=True)
class PriceMark:
    instrument_id: str
    currency: str
    price: Decimal
    business_date: date

    def __post_init__(self) -> None:
        _identifier(self.instrument_id)
        _currency(self.currency)
        _number(self.price, "1e9", 6, positive=True)
        _date(self.business_date)


@dataclass(frozen=True)
class FxMark:
    currency: str
    usd_per_unit: Decimal
    business_date: date

    def __post_init__(self) -> None:
        if self.currency != "CAD":
            raise ValueError("Only CAD needs an explicit USD-per-unit FX mark")
        _number(self.usd_per_unit, "1e3", 8, positive=True)
        _date(self.business_date)


@dataclass(frozen=True)
class Cash:
    currency: str
    amount: Decimal

    def __post_init__(self) -> None:
        _currency(self.currency)
        _number(self.amount, "1e15", 2)


@dataclass(frozen=True)
class QualityIssue:
    code: str
    subject: str


@dataclass(frozen=True)
class ValuationLine:
    subject: str
    value_usd: Decimal


@dataclass(frozen=True)
class Valuation:
    snapshot_id: str
    business_date: date
    total_usd: Decimal | None
    lines: tuple[ValuationLine, ...]
    issues: tuple[QualityIssue, ...]
    data_kind: str = "synthetic"

    def to_dict(self) -> dict:
        """Serialize financial amounts as decimal strings, preserving USD units."""
        return {
            "snapshot_id": self.snapshot_id,
            "business_date": self.business_date.isoformat(),
            "data_kind": self.data_kind,
            "reporting_currency": "USD",
            "status": "blocked" if self.issues else "complete",
            "total_usd": None if self.total_usd is None else str(self.total_usd),
            "lines": [
                {"subject": line.subject, "value_usd": str(line.value_usd)}
                for line in self.lines
            ],
            "issues": [
                {"code": issue.code, "subject": issue.subject} for issue in self.issues
            ],
        }


def _index(items: tuple, item_type: type, key: str) -> dict:
    if not isinstance(items, tuple) or len(items) > 10000:
        raise ValueError("Snapshot collections must be tuples of at most 10,000 items")
    result = {}
    for item in items:
        if type(item) is not item_type:
            raise ValueError(f"Expected {item_type.__name__} items")
        identifier = getattr(item, key)
        if identifier in result:
            raise ValueError(f"Duplicate {item_type.__name__} key: {identifier}")
        result[identifier] = item
    return result


def value_snapshot(
    *,
    snapshot_id: str,
    business_date: date,
    holdings: tuple[Holding, ...],
    prices: tuple[PriceMark, ...],
    fx: tuple[FxMark, ...] = (),
    cash: tuple[Cash, ...] = (),
) -> Valuation:
    """Value an explicitly synthetic snapshot, blocking totals on missing/stale marks.

    Complete totals are summed before rounding. Lines are displayed rounded and
    may not add to that total. Blocked results contain no partial values.
    """
    _identifier(snapshot_id)
    _date(business_date)
    positions = _index(holdings, Holding, "instrument_id")
    marks = _index(prices, PriceMark, "instrument_id")
    rates = _index(fx, FxMark, "currency")
    balances = _index(cash, Cash, "currency")
    issues: list[QualityIssue] = []
    raw_lines: list[tuple[str, Decimal]] = []

    def rate(currency: str, subject: str) -> Decimal | None:
        if currency == "USD":
            return Decimal(1)
        mark = rates.get(currency)
        if mark is None:
            issues.append(QualityIssue("MISSING_FX", subject))
            return None
        if mark.business_date != business_date:
            issues.append(QualityIssue("FX_DATE_MISMATCH", subject))
            return None
        return mark.usd_per_unit

    with localcontext(Context(prec=64, rounding=ROUND_HALF_EVEN)):
        for identifier, holding in positions.items():
            mark = marks.get(identifier)
            subject = f"security:{identifier}"
            if mark is None:
                issues.append(QualityIssue("MISSING_PRICE", subject))
                continue
            if mark.business_date != business_date:
                issues.append(QualityIssue("PRICE_DATE_MISMATCH", subject))
                continue
            conversion = rate(mark.currency, subject)
            if conversion is not None:
                raw_lines.append((subject, holding.quantity * mark.price * conversion))
        for currency, balance in balances.items():
            subject = f"cash:{currency}"
            conversion = rate(currency, subject)
            if conversion is not None:
                raw_lines.append((subject, balance.amount * conversion))
        if issues:
            return Valuation(snapshot_id, business_date, None, (), tuple(issues))
        total = sum((value for _, value in raw_lines), Decimal(0)).quantize(CENT)
        lines = tuple(
            ValuationLine(subject, value.quantize(CENT)) for subject, value in raw_lines
        )
        return Valuation(snapshot_id, business_date, total, lines, ())
