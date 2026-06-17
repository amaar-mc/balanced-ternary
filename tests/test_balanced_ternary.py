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


# ---------------------------------------------------------------------------
# Ordering: __lt__, __le__, __gt__, __ge__
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a,b",
    [
        (-5, -3),
        (-3, 0),
        (0, 1),
        (1, 7),
        (-1000, 1000),
        (0, 0),
        (3, 3),
        (-7, -7),
        (-1, 1),
        (9, 10),
    ],
)
def test_lt_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) < BalancedTernary(b) matches a < b."""
    assert (BalancedTernary.from_int(a) < BalancedTernary.from_int(b)) == (a < b)


@pytest.mark.parametrize(
    "a,b",
    [
        (-5, -3),
        (-3, 0),
        (0, 1),
        (1, 7),
        (-1000, 1000),
        (0, 0),
        (3, 3),
        (-7, -7),
        (-1, 1),
        (9, 10),
    ],
)
def test_le_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) <= BalancedTernary(b) matches a <= b."""
    assert (BalancedTernary.from_int(a) <= BalancedTernary.from_int(b)) == (a <= b)


@pytest.mark.parametrize(
    "a,b",
    [
        (-5, -3),
        (-3, 0),
        (0, 1),
        (1, 7),
        (-1000, 1000),
        (0, 0),
        (3, 3),
        (-7, -7),
        (-1, 1),
        (9, 10),
    ],
)
def test_gt_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) > BalancedTernary(b) matches a > b."""
    assert (BalancedTernary.from_int(a) > BalancedTernary.from_int(b)) == (a > b)


@pytest.mark.parametrize(
    "a,b",
    [
        (-5, -3),
        (-3, 0),
        (0, 1),
        (1, 7),
        (-1000, 1000),
        (0, 0),
        (3, 3),
        (-7, -7),
        (-1, 1),
        (9, 10),
    ],
)
def test_ge_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) >= BalancedTernary(b) matches a >= b."""
    assert (BalancedTernary.from_int(a) >= BalancedTernary.from_int(b)) == (a >= b)


def test_sorting_matches_int() -> None:
    """Sorting a list of BalancedTernary matches sorting their int values."""
    values = [-7, 0, 5, -1, 3, -100, 100, 1, -1]
    bt_list = [BalancedTernary.from_int(v) for v in values]
    sorted_bt = sorted(bt_list)
    sorted_ints = sorted(values)
    assert [x.to_int() for x in sorted_bt] == sorted_ints


def test_sorting_empty_and_single() -> None:
    """Sorting zero or one BalancedTernary works."""
    assert sorted([]) == []
    one = [BalancedTernary.from_int(42)]
    assert sorted(one) == one


def test_ordering_consistency_with_eq() -> None:
    """Ordering is consistent: a == b implies not (a < b) and not (a > b)."""
    for n in [-10, -1, 0, 1, 10]:
        a = BalancedTernary.from_int(n)
        b = BalancedTernary.from_int(n)
        assert a == b
        assert not (a < b)
        assert not (a > b)
        assert a <= b
        assert a >= b


def test_lt_non_bt_returns_not_implemented() -> None:
    """__lt__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    assert bt.__lt__(42) is NotImplemented


def test_le_non_bt_returns_not_implemented() -> None:
    """__le__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    assert bt.__le__(42) is NotImplemented


def test_gt_non_bt_returns_not_implemented() -> None:
    """__gt__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    assert bt.__gt__(42) is NotImplemented


def test_ge_non_bt_returns_not_implemented() -> None:
    """__ge__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(1)
    assert bt.__ge__(42) is NotImplemented


@given(a=_ints, b=_ints)
@settings(max_examples=500)
def test_lt_oracle(a: int, b: int) -> None:
    """BalancedTernary comparison matches int comparison."""
    assert (BalancedTernary.from_int(a) < BalancedTernary.from_int(b)) == (a < b)


@given(a=_ints, b=_ints)
@settings(max_examples=300)
def test_ordering_total(a: int, b: int) -> None:
    """Total ordering: exactly one of a<b, a==b, a>b holds."""
    ba = BalancedTernary.from_int(a)
    bb = BalancedTernary.from_int(b)
    lt = ba < bb
    eq = ba == bb
    gt = ba > bb
    assert (lt, eq, gt).count(True) == 1


# ---------------------------------------------------------------------------
# Division: __floordiv__, __mod__, __divmod__
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a,b",
    [
        (7, 2),
        (7, -2),
        (-7, 2),
        (-7, -2),
        (0, 5),
        (0, -5),
        (9, 3),
        (-9, 3),
        (9, -3),
        (-9, -3),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
        (10, 3),
        (-10, 3),
        (10, -3),
        (-10, -3),
        (100, 7),
        (-100, 7),
        (100, -7),
        (-100, -7),
    ],
)
def test_floordiv_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) // BalancedTernary(b) matches a // b."""
    result = BalancedTernary.from_int(a) // BalancedTernary.from_int(b)
    assert result.to_int() == a // b


@pytest.mark.parametrize(
    "a,b",
    [
        (7, 2),
        (7, -2),
        (-7, 2),
        (-7, -2),
        (0, 5),
        (0, -5),
        (9, 3),
        (-9, 3),
        (9, -3),
        (-9, -3),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
        (10, 3),
        (-10, 3),
        (10, -3),
        (-10, -3),
        (100, 7),
        (-100, 7),
        (100, -7),
        (-100, -7),
    ],
)
def test_mod_parametrized(a: int, b: int) -> None:
    """BalancedTernary(a) % BalancedTernary(b) matches a % b."""
    result = BalancedTernary.from_int(a) % BalancedTernary.from_int(b)
    assert result.to_int() == a % b


@pytest.mark.parametrize(
    "a,b",
    [
        (7, 2),
        (7, -2),
        (-7, 2),
        (-7, -2),
        (9, 3),
        (-9, 3),
        (10, 3),
        (-10, 3),
        (100, 7),
        (-100, 7),
    ],
)
def test_divmod_identity(a: int, b: int) -> None:
    """a == (a // b) * b + (a % b) holds on BalancedTernary objects."""
    ba = BalancedTernary.from_int(a)
    bb = BalancedTernary.from_int(b)
    q, r = divmod(ba, bb)
    assert (q * bb + r).to_int() == a


def test_floordiv_zero_raises() -> None:
    """Division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        BalancedTernary.from_int(5) // BalancedTernary.from_int(0)


def test_mod_zero_raises() -> None:
    """Modulo by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        BalancedTernary.from_int(5) % BalancedTernary.from_int(0)


def test_divmod_zero_raises() -> None:
    """divmod by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divmod(BalancedTernary.from_int(5), BalancedTernary.from_int(0))


def test_floordiv_non_bt_returns_not_implemented() -> None:
    """__floordiv__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(5)
    assert bt.__floordiv__(2) is NotImplemented


def test_mod_non_bt_returns_not_implemented() -> None:
    """__mod__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(5)
    assert bt.__mod__(2) is NotImplemented


def test_divmod_non_bt_returns_not_implemented() -> None:
    """__divmod__ with non-BalancedTernary returns NotImplemented."""
    bt = BalancedTernary.from_int(5)
    assert bt.__divmod__(2) is NotImplemented


def test_remainder_sign_convention_positive_divisor() -> None:
    """Remainder has sign of divisor when divisor is positive (Python floored)."""
    for a in [-7, -6, -1, 0, 1, 6, 7]:
        r = (BalancedTernary.from_int(a) % BalancedTernary.from_int(3)).to_int()
        assert 0 <= r < 3, f"remainder {r} out of range for a={a}, b=3"


def test_remainder_sign_convention_negative_divisor() -> None:
    """Remainder has sign of divisor when divisor is negative (Python floored)."""
    for a in [-7, -6, -1, 0, 1, 6, 7]:
        r = (BalancedTernary.from_int(a) % BalancedTernary.from_int(-3)).to_int()
        assert -3 < r <= 0, f"remainder {r} out of range for a={a}, b=-3"


@given(
    a=_ints,
    b=st.integers(min_value=-500, max_value=500).filter(lambda x: x != 0),
)
@settings(max_examples=500)
def test_floordiv_oracle(a: int, b: int) -> None:
    """BalancedTernary floordiv matches int floordiv."""
    result = (BalancedTernary.from_int(a) // BalancedTernary.from_int(b)).to_int()
    assert result == a // b


@given(
    a=_ints,
    b=st.integers(min_value=-500, max_value=500).filter(lambda x: x != 0),
)
@settings(max_examples=500)
def test_mod_oracle(a: int, b: int) -> None:
    """BalancedTernary mod matches int mod."""
    assert (BalancedTernary.from_int(a) % BalancedTernary.from_int(b)).to_int() == a % b


@given(
    a=_ints,
    b=st.integers(min_value=-500, max_value=500).filter(lambda x: x != 0),
)
@settings(max_examples=500)
def test_divmod_identity_hypothesis(a: int, b: int) -> None:
    """a == (a // b) * b + (a % b) holds for all nonzero b."""
    ba = BalancedTernary.from_int(a)
    bb = BalancedTernary.from_int(b)
    q, r = divmod(ba, bb)
    assert (q * bb + r).to_int() == a
