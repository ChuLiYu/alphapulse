"""Independent VAL-01–05 examples and boundary failures; no external services."""

from datetime import date, datetime
from decimal import Decimal, Inexact, Rounded, getcontext, localcontext, ROUND_UP
import json
import unittest

from alphapulse.portfolio.valuation import (
    Cash,
    FxMark,
    Holding,
    PriceMark,
    value_snapshot,
)

D = Decimal
DAY = date(2026, 10, 29)


class ValuationTests(unittest.TestCase):
    def value(self, **overrides):
        arguments = dict(
            snapshot_id="synthetic-test",
            business_date=DAY,
            holdings=(Holding("A", D("10")), Holding("B", D("2"))),
            prices=(
                PriceMark("A", "USD", D("100.005"), DAY),
                PriceMark("B", "CAD", D("50"), DAY),
            ),
            fx=(FxMark("CAD", D("0.75"), DAY),),
            cash=(Cash("USD", D("25")),),
        )
        arguments.update(overrides)
        return value_snapshot(**arguments)

    def test_golden_multi_currency_total_and_cash(self):
        result = self.value()
        self.assertEqual(result.total_usd, D("1100.05"))
        self.assertEqual(
            [line.value_usd for line in result.lines],
            [D("1000.05"), D("75.00"), D("25.00")],
        )
        self.assertEqual(result.issues, ())

    def test_sum_before_rounding_and_half_even(self):
        result = self.value(
            holdings=(Holding("A", D(1)), Holding("B", D(1))),
            prices=(
                PriceMark("A", "USD", D("0.005"), DAY),
                PriceMark("B", "USD", D("0.005"), DAY),
            ),
            cash=(),
            fx=(),
        )
        self.assertEqual(result.total_usd, D("0.01"))
        self.assertEqual(
            [line.value_usd for line in result.lines], [D("0.00"), D("0.00")]
        )
        result = self.value(
            holdings=(Holding("A", D(1)),),
            prices=(PriceMark("A", "USD", D("1.015"), DAY),),
            cash=(),
        )
        self.assertEqual(result.total_usd, D("1.02"))

    def test_cash_fx_and_empty_snapshot(self):
        self.assertEqual(
            self.value(holdings=(), prices=(), cash=(Cash("CAD", D("100")),)).total_usd,
            D("75.00"),
        )
        self.assertEqual(
            self.value(holdings=(), prices=(), cash=(), fx=()).total_usd, D("0.00")
        )

    def test_missing_price_blocks_every_value(self):
        result = self.value(prices=(PriceMark("A", "USD", D("100.005"), DAY),))
        self.assertIsNone(result.total_usd)
        self.assertEqual(result.lines, ())
        self.assertEqual(
            [(i.code, i.subject) for i in result.issues],
            [("MISSING_PRICE", "security:B")],
        )

    def test_missing_fx_blocks_security_and_cash(self):
        result = self.value(fx=(), cash=(Cash("CAD", D("5")),))
        self.assertIsNone(result.total_usd)
        self.assertEqual([i.code for i in result.issues], ["MISSING_FX", "MISSING_FX"])

    def test_stale_and_future_prices_block(self):
        for day in (date(2026, 10, 28), date(2026, 10, 30)):
            with self.subTest(day=day):
                result = self.value(
                    prices=(
                        PriceMark("A", "USD", D(1), day),
                        PriceMark("B", "CAD", D(1), DAY),
                    )
                )
                self.assertIsNone(result.total_usd)
                self.assertEqual(result.issues[0].code, "PRICE_DATE_MISMATCH")

    def test_stale_and_future_fx_block(self):
        for day in (date(2026, 10, 28), date(2026, 10, 30)):
            result = self.value(fx=(FxMark("CAD", D("0.75"), day),))
            self.assertIsNone(result.total_usd)
            self.assertEqual(result.issues[0].code, "FX_DATE_MISMATCH")

    def test_float_string_nonfinite_and_negative_rejected(self):
        for value in (0.1, "0.1", D("NaN"), D("Infinity"), D("-Infinity"), D("-0.1")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Holding("A", value)
        for factory in (
            lambda: PriceMark("A", "USD", D(0), DAY),
            lambda: FxMark("CAD", D(0), DAY),
            lambda: Cash("USD", D(-1)),
        ):
            with self.assertRaises(ValueError):
                factory()

    def test_precision_and_maximum_bounds(self):
        invalid = (
            lambda: Holding("A", D("1e13")),
            lambda: Holding("A", D("0.0000001")),
            lambda: PriceMark("A", "USD", D("1e10"), DAY),
            lambda: PriceMark("A", "USD", D("0.0000001"), DAY),
            lambda: FxMark("CAD", D("1001"), DAY),
            lambda: FxMark("CAD", D("0.000000001"), DAY),
            lambda: Cash("USD", D("1e16")),
            lambda: Cash("USD", D("0.001")),
        )
        for factory in invalid:
            with self.assertRaises(ValueError):
                factory()
        result = self.value(
            holdings=(Holding("A", D("1e12")),),
            prices=(PriceMark("A", "CAD", D("1e9"), DAY),),
            fx=(FxMark("CAD", D("1e3"), DAY),),
            cash=(),
        )
        self.assertEqual(result.total_usd, D("1000000000000000000000000.00"))

    def test_duplicate_identifiers_are_not_silently_merged(self):
        cases = dict(
            holdings=(Holding("A", D(1)), Holding("A", D(2))),
            prices=(PriceMark("A", "USD", D(1), DAY), PriceMark("A", "USD", D(2), DAY)),
            fx=(FxMark("CAD", D(1), DAY), FxMark("CAD", D(2), DAY)),
            cash=(Cash("USD", D(1)), Cash("USD", D(2))),
        )
        for key, value in cases.items():
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.value(**{key: value})

    def test_unsupported_currency_and_bad_identity_or_date(self):
        for factory in (
            lambda: PriceMark("A", "EUR", D(1), DAY),
            lambda: FxMark("USD", D(1), DAY),
            lambda: Cash("EUR", D(1)),
            lambda: Holding(" ", D(1)),
            lambda: Cash([], D(1)),
            lambda: PriceMark("A", "USD", D(1), datetime(2026, 10, 29)),
            lambda: self.value(snapshot_id=""),
            lambda: self.value(business_date="2026-10-29"),
        ):
            with self.assertRaises(ValueError):
                factory()

    def test_collections_require_valid_typed_bounded_items(self):
        for items in ([Holding("A", D(1))], (object(),), (Holding("A", D(1)),) * 10001):
            with self.assertRaises(ValueError):
                self.value(holdings=items)

    def test_calculation_is_independent_of_callers_decimal_context(self):
        with localcontext() as context:
            context.prec = 3
            context.rounding = ROUND_UP
            context.traps[Inexact] = True
            context.traps[Rounded] = True
            self.assertEqual(self.value().total_usd, D("1100.05"))
            self.assertEqual(getcontext().prec, 3)
            self.assertEqual(getcontext().rounding, ROUND_UP)
            self.assertTrue(getcontext().traps[Inexact])

    def test_json_strings_and_synthetic_provenance(self):
        body = json.loads(json.dumps(self.value().to_dict()))
        self.assertEqual(body["total_usd"], "1100.05")
        self.assertEqual(body["reporting_currency"], "USD")
        self.assertEqual(body["data_kind"], "synthetic")
        self.assertEqual(body["business_date"], "2026-10-29")
        self.assertEqual(body["snapshot_id"], "synthetic-test")
        self.assertIsNone(self.value(fx=()).to_dict()["total_usd"])
        self.assertEqual(self.value(fx=()).to_dict()["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
