"""
Tests for the TimeString class.

"""
import unittest

from sharpe.analysis.timestring import TimeString


class TestUnitValue(unittest.TestCase):
    """Tests the TimeString.unit_value() method."""

    def test_improper_format(self):
        """Tests that improperly formatted timestrings raise a ValueError."""
        cases = ("3m3", "t3", "3.03", "3", "3.03m", "-3", "-3m", "-3.03d", "3min", "30minute")
        ts: TimeString
        for case in cases:
            ts = TimeString(case)
            with self.assertRaises(ValueError):
                ts.unit_value()

    def test_proper_format(self):
        """Tests that properly formatted timestrings produce a unit and integer value."""
        cases = (
            ("1m", ("m", 1)),
            ("60m", ("m", 60)),
            ("5d", ("d", 5)),
            ("1wk", ("wk", 1)),
            ("12mo", ("mo", 12)),
        )
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.unit_value()
            self.assertTupleEqual(expected_result, result)


class TestPandasOffsetAlias(unittest.TestCase):
    """Tests the TimeString.pandas_offset_alias property."""

    def test_minute_conversions(self):
        """Tests conversions for minute time strings."""
        cases = (("1m", "1T"), ("15m", "15T"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_hour_conversions(self):
        """Tests conversions for hour time strings."""
        cases = (("1h", "1H"), ("12h", "12H"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_day_conversions(self):
        """Tests conversions for day time strings."""
        cases = (("1d", "1D"), ("10d", "10D"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_week_conversions(self):
        """Tests conversions for week time strings."""
        cases = (("1wk", "1W"), ("12wk", "12W"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_month_conversions(self):
        """Tests conversions for month time strings."""
        cases = (("1mo", "1M"), ("12mo", "12M"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_year_conversions(self):
        """Tests conversions for year time strings."""
        cases = (("1y", "1Y"), ("10y", "10Y"))
        ts: TimeString
        for arg, expected_result in cases:
            ts = TimeString(arg)
            result = ts.pandas_offset_alias(prepend_value=True)
            self.assertEqual(expected_result, result)

    def test_unsupported_unit_conversions(self):
        """Tests that conversion attempts for unsupported units raise a KeyError or ValueError."""
        cases = ("1min", "10min", "1Q", "12Q")
        ts: TimeString
        for case in cases:
            ts = TimeString(case)
            with self.assertRaises((KeyError, ValueError)):
                ts.pandas_offset_alias(prepend_value=True)
