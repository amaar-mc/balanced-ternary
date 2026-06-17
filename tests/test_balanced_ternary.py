"""Tests for the balanced_ternary package.

Coverage:
- Golden values specified in the project requirements
- Round-trip conversions (int->BT->int, str->BT->str)
- Digit-level arithmetic verified against int oracle via Hypothesis
- Negation, addition, subtraction, multiplication
- Error handling for invalid inputs
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from balanced_ternary import BalancedTernary

# ---------------------------------------------------------------------------
# Golden values
# ---------------------------------------------------------------------------


def test_golden_5() -> None:
    """from_int(5) must produce '1TT'."""
    assert BalancedTernary.from_int(5).to_str() == "1TT"


def test_golden_neg7() -> None:
    """from_int(-7) must produce 'T1T'."""
    assert BalancedTernary.from_int(-7).to_str() == "T1T"


def test_golden_2() -> None:
    """from_int(2) must produce '1T'."""
    assert BalancedTernary.from_int(2).to_str() == "1T"


def test_golden_0() -> None:
    """from_int(0) must produce '0'."""
    assert BalancedTernary.from_int(0).to_str() == "0"


def test_golden_1() -> None:
    """from_int(1) must produce '1'."""
    assert BalancedTernary.from_int(1).to_str() == "1"


# ---------------------------------------------------------------------------
# Round-trip: int -> BalancedTernary -> int
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("n", range(-1000, 1001))
def test_round_trip_int(n: int) -> None:
    """from_int(n).to_int() == n for n in -1000..1000."""
    assert BalancedTernary.from_int(n).to_int() == n


# ---------------------------------------------------------------------------
# Round-trip: str -> BalancedTernary -> str
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "s",
    [
        "0",
        "1",
        "T",
        "1T",
        "10",
        "11",
        "1TT",
        "T1T",
        "101",
        "1T0T1",
        "TTT",
        "111",
    ],
)
def test_round_trip_str(s: str) -> None:
    """from_str(s).to_str() == s for canonical strings."""
    assert BalancedTernary.from_str(s).to_str() == s


def test_from_str_lowercase_t() -> None:
    """from_str accepts lowercase 't' as -1."""
    bt = BalancedTernary.from_str("1t")
    assert bt.to_int() == 2
    assert bt.to_str() == "1T"


def test_from_str_strips_leading_zeros() -> None:
    """from_str normalizes leading zeros."""
    assert BalancedTernary.from_str("001").to_str() == "1"
    assert BalancedTernary.from_str("000").to_str() == "0"


# ---------------------------------------------------------------------------
# Specific arithmetic identities
# ---------------------------------------------------------------------------


def test_add_5_plus_neg3() -> None:
    """from_int(5) + from_int(-3) == from_int(2)."""
    result = BalancedTernary.from_int(5) + BalancedTernary.from_int(-3)
    assert result == BalancedTernary.from_int(2)


def test_negation_fixed() -> None:
    """Negation of specific values."""
    assert (-BalancedTernary.from_int(5)).to_int() == -5
    assert (-BalancedTernary.from_int(0)).to_int() == 0
    assert (-BalancedTernary.from_int(-7)).to_int() == 7


# ---------------------------------------------------------------------------
# Hypothesis: arithmetic vs int oracle
# ---------------------------------------------------------------------------

_ints = st.integers(min_value=-500, max_value=500)


@given(a=_ints, b=_ints)
@settings(max_examples=500)
def test_add_oracle(a: int, b: int) -> None:
    """(from_int(a) + from_int(b)).to_int() == a + b."""
    result = (BalancedTernary.from_int(a) + BalancedTernary.from_int(b)).to_int()
    assert result == a + b


@given(a=_ints, b=_ints)
@settings(max_examples=500)
def test_sub_oracle(a: int, b: int) -> None:
    """(from_int(a) - from_int(b)).to_int() == a - b."""
    result = (BalancedTernary.from_int(a) - BalancedTernary.from_int(b)).to_int()
    assert result == a - b


@given(a=_ints, b=_ints)
@settings(max_examples=500)
def test_mul_oracle(a: int, b: int) -> None:
    """(from_int(a) * from_int(b)).to_int() == a * b."""
    result = (BalancedTernary.from_int(a) * BalancedTernary.from_int(b)).to_int()
    assert result == a * b


@given(a=_ints)
@settings(max_examples=300)
def test_neg_oracle(a: int) -> None:
    """(-from_int(a)).to_int() == -a."""
    assert (-BalancedTernary.from_int(a)).to_int() == -a


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_from_str_empty_raises() -> None:
    """from_str raises ValueError on empty string."""
    with pytest.raises(ValueError, match="non-empty"):
        BalancedTernary.from_str("")


@pytest.mark.parametrize("bad", ["2", "a", "1X0", "-1", " ", "1 0"])
def test_from_str_invalid_char_raises(bad: str) -> None:
    """from_str raises ValueError on invalid characters."""
    with pytest.raises(ValueError, match="Invalid character"):
        BalancedTernary.from_str(bad)


# ---------------------------------------------------------------------------
# Equality and hashing
# ---------------------------------------------------------------------------


def test_equality() -> None:
    """Equal balanced ternary values compare equal."""
    a = BalancedTernary.from_int(42)
    b = BalancedTernary.from_int(42)
    assert a == b
    assert a == b


def test_inequality() -> None:
    """Different values are not equal."""
    assert BalancedTernary.from_int(1) != BalancedTernary.from_int(2)


def test_hash_consistent_with_equality() -> None:
    """Equal objects have the same hash."""
    a = BalancedTernary.from_int(99)
    b = BalancedTernary.from_int(99)
    assert hash(a) == hash(b)


def test_usable_as_dict_key() -> None:
    """BalancedTernary instances can be used as dict keys."""
    d: dict[BalancedTernary, str] = {BalancedTernary.from_int(1): "one"}
    assert d[BalancedTernary.from_int(1)] == "one"


# ---------------------------------------------------------------------------
# __repr__ and __str__
# ---------------------------------------------------------------------------


def test_repr() -> None:
    """repr produces a parseable string."""
    bt = BalancedTernary.from_int(5)
    assert repr(bt) == "BalancedTernary.from_str('1TT')"


def test_str() -> None:
    """str returns the T-notation string."""
    assert str(BalancedTernary.from_int(5)) == "1TT"


# ---------------------------------------------------------------------------
# Type safety: arithmetic with non-BalancedTernary returns NotImplemented
# ---------------------------------------------------------------------------


def test_add_non_bt_returns_not_implemented() -> None:
    """Adding a non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    result = bt.__add__(42)
    assert result is NotImplemented


def test_mul_non_bt_returns_not_implemented() -> None:
    """Multiplying a non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    result = bt.__mul__("x")
    assert result is NotImplemented


def test_sub_non_bt_returns_not_implemented() -> None:
    """Subtracting a non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    result = bt.__sub__(1.0)
    assert result is NotImplemented
