"""Run a fixed synthetic investment snapshot; never fetch or imply live prices."""

from datetime import date
from decimal import Decimal
import json

from alphapulse.portfolio.valuation import (
    Cash,
    FxMark,
    Holding,
    PriceMark,
    value_snapshot,
)


def main() -> None:
    business_date = date(2026, 10, 29)
    result = value_snapshot(
        snapshot_id="synthetic-balanced-001",
        business_date=business_date,
        holdings=(Holding("US-EQUITY", Decimal("10")), Holding("CA-ETF", Decimal("2"))),
        prices=(
            PriceMark("US-EQUITY", "USD", Decimal("100.005"), business_date),
            PriceMark("CA-ETF", "CAD", Decimal("50"), business_date),
        ),
        fx=(FxMark("CAD", Decimal("0.75"), business_date),),
        cash=(Cash("USD", Decimal("25")),),
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
