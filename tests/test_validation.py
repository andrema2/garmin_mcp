import re

import pytest

from garmin_mcp.utils.validation import (
    validate_date,
    validate_date_range,
    resolve_date,
)
from garmin_mcp.utils.errors import GarminValidationError


def test_validate_date_ok():
    assert validate_date("2024-01-15") == "2024-01-15"


@pytest.mark.parametrize(
    "value",
    [
        "2024-1-1",
        "2024/01/01",
        "2024-13-01",
        "not-a-date",
        "",
        "   ",
    ],
)
def test_validate_date_invalid(value):
    with pytest.raises(GarminValidationError):
        validate_date(value, "date")


def test_validate_date_range_ok():
    assert validate_date_range("2024-01-01", "2024-01-02") == ("2024-01-01", "2024-01-02")


def test_validate_date_range_start_after_end():
    with pytest.raises(GarminValidationError):
        validate_date_range("2024-01-02", "2024-01-01")


def test_resolve_date_defaults_to_today():
    today = resolve_date(None)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", today)


def test_resolve_date_empty_defaults_to_today():
    today = resolve_date("   ")
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", today)


def test_resolve_date_validates_when_provided():
    assert resolve_date("2024-02-29") == "2024-02-29"


