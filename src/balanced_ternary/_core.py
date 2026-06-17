"""Core implementation of the BalancedTernary number type.

Balanced ternary uses digits from the set {-1, 0, 1}, where -1 is written as
'T' (or 't') in T-notation. Arithmetic is implemented at the digit level using
balanced ternary carry logic, not by converting to int and back.

Internally, digits are stored as a list of ints in least-significant-first
order, normalized to remove leading zeros (trailing zeros in the internal list),
except that zero is stored as [0].
"""

from __future__ import annotations

from typing import Final

# Carry table: maps a digit sum s to (result_digit, carry_out)
# s can range from -3 to 3 when adding two balanced-ternary digits plus carry.
_CARRY_TABLE: Final[dict[int, tuple[int, int]]] = {
    -3: (0, -1),
    -2: (1, -1),
    -1: (-1, 0),
    0: (0, 0),
    1: (1, 0),
    2: (-1, 1),
    3: (0, 1),
}


def _normalize(digits: list[int]) -> list[int]:
    """Remove trailing zeros (most-significant zeros) from the digit list.

    The internal representation is least-significant-first, so trailing
    elements in the list correspond to the most significant positions.
    The result always has at least one element.

    Args:
        digits: Digit list in least-significant-first order.

    Returns:
        Normalized digit list with no leading-zero positions, minimum length 1.
    """
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits


def _add_digits(a: list[int], b: list[int]) -> list[int]:
    """Add two digit lists using balanced-ternary carry logic.

    Args:
        a: Digits of the first operand, least-significant-first.
        b: Digits of the second operand, least-significant-first.

    Returns:
        Normalized digit list of the sum.
    """
    length = max(len(a), len(b))
    result: list[int] = []
    carry = 0
    for i in range(length):
        da = a[i] if i < len(a) else 0
        db = b[i] if i < len(b) else 0
        s = da + db + carry
        digit, carry = _CARRY_TABLE[s]
        result.append(digit)
    if carry != 0:
        result.append(carry)
    return _normalize(result)


def _negate_digits(digits: list[int]) -> list[int]:
    """Negate a digit list by flipping every digit sign.

    In balanced ternary, negation is exact: flip -1 <-> 1 and leave 0 as 0.
    No carry is needed.

    Args:
        digits: Digits in least-significant-first order.

    Returns:
        Negated digit list (already normalized since negation preserves length).
    """
    return [-d for d in digits]


def _mul_digits(a: list[int], b: list[int]) -> list[int]:
    """Multiply two digit lists using digit-by-digit accumulation.

    For each digit b_i of b, compute a * b_i shifted left by i positions,
    then accumulate all partial products using balanced-ternary addition.

    Args:
        a: Digits of the first operand, least-significant-first.
        b: Digits of the second operand, least-significant-first.

    Returns:
        Normalized digit list of the product.
    """
    accumulator: list[int] = [0]
    for i, db in enumerate(b):
        if db == 0:
            continue
        # Partial product: a * db, shifted left by i positions
        partial: list[int] = [0] * i + [da * db for da in a]
        # a * db where db in {-1, 1} keeps each digit in {-1, 0, 1}; no carry needed
        accumulator = _add_digits(accumulator, partial)
    return _normalize(accumulator)


class BalancedTernary:
    """An immutable balanced ternary integer.

    Balanced ternary represents integers using digits from {-1, 0, 1}.
    The digit -1 is written as 'T' in T-notation. Arithmetic operations
    are implemented at the digit level with balanced-ternary carry logic.

    Attributes:
        _digits: Internal storage, least-significant-first list of ints
                 from {-1, 0, 1}, normalized (no trailing zeros except
                 the canonical zero representation [0]).
    """

    __slots__ = ("_digits",)

    def __init__(self, digits: list[int]) -> None:
        """Initialize from a normalized, least-significant-first digit list.

        This constructor is internal. Use from_int or from_str instead.

        Args:
            digits: Normalized digit list, each element in {-1, 0, 1}.

        Raises:
            ValueError: If any digit is not in {-1, 0, 1}.
        """
        for d in digits:
            if d not in (-1, 0, 1):
                raise ValueError(
                    f"Each digit must be in {{-1, 0, 1}}, got {d!r}"
                )
        self._digits: list[int] = digits

    @classmethod
    def from_int(cls, value: int) -> BalancedTernary:
        """Convert a Python int to balanced ternary.

        Uses the standard balanced-ternary conversion: repeatedly divide by 3
        using balanced remainders in {-1, 0, 1}.

        Args:
            value: Any Python integer.

        Returns:
            BalancedTernary representation of value.
        """
        if value == 0:
            return cls([0])
        digits: list[int] = []
        n = value
        while n != 0:
            remainder = n % 3
            if remainder == 2:
                remainder = -1
            elif remainder == -2:
                remainder = 1
            digits.append(remainder)
            n = (n - remainder) // 3
        return cls(_normalize(digits))

    @classmethod
    def from_str(cls, text: str) -> BalancedTernary:
        """Parse a T-notation string into balanced ternary.

        Digits are: '1' for +1, '0' for 0, 'T' or 't' for -1.
        The string is most-significant-first. Leading zeros are allowed
        but the result is normalized. The empty string is rejected.

        Args:
            text: Non-empty string of digits '0', '1', 'T', 't'.

        Returns:
            BalancedTernary represented by the string.

        Raises:
            ValueError: If text is empty or contains an invalid character.
        """
        if not text:
            raise ValueError(
                "from_str requires a non-empty string, got an empty string"
            )
        digits_msb: list[int] = []
        for ch in text:
            if ch == "1":
                digits_msb.append(1)
            elif ch == "0":
                digits_msb.append(0)
            elif ch in ("T", "t"):
                digits_msb.append(-1)
            else:
                raise ValueError(
                    f"Invalid character {ch!r} in balanced ternary string {text!r}; "
                    f"expected '0', '1', 'T', or 't'"
                )
        # Reverse to get least-significant-first
        digits_lsf = list(reversed(digits_msb))
        return cls(_normalize(digits_lsf))

    def to_int(self) -> int:
        """Convert to a Python int.

        Returns:
            The integer value of this balanced ternary number.
        """
        result = 0
        power = 1
        for d in self._digits:
            result += d * power
            power *= 3
        return result

    def to_str(self) -> str:
        """Convert to canonical T-notation string.

        Digits are most-significant-first. The digit -1 is written as 'T'.
        The only string with a leading zero is "0".

        Returns:
            Canonical T-notation string.
        """
        chars: list[str] = []
        for d in reversed(self._digits):
            if d == 1:
                chars.append("1")
            elif d == 0:
                chars.append("0")
            else:
                chars.append("T")
        return "".join(chars)

    def __neg__(self) -> BalancedTernary:
        """Return the negation of this value.

        Returns:
            A new BalancedTernary with each digit sign-flipped.
        """
        return BalancedTernary(_normalize(_negate_digits(list(self._digits))))

    def __add__(self, other: object) -> BalancedTernary:
        """Return self + other using digit-level balanced-ternary addition.

        Args:
            other: Another BalancedTernary instance.

        Returns:
            The sum as a new BalancedTernary.

        Raises:
            TypeError: If other is not a BalancedTernary.
        """
        if not isinstance(other, BalancedTernary):
            return NotImplemented
        return BalancedTernary(_add_digits(list(self._digits), list(other._digits)))

    def __sub__(self, other: object) -> BalancedTernary:
        """Return self - other.

        Subtraction is implemented as self + (-other).

        Args:
            other: Another BalancedTernary instance.

        Returns:
            The difference as a new BalancedTernary.

        Raises:
            TypeError: If other is not a BalancedTernary.
        """
        if not isinstance(other, BalancedTernary):
            return NotImplemented
        return self + (-other)

    def __mul__(self, other: object) -> BalancedTernary:
        """Return self * other using digit-level balanced-ternary multiplication.

        Args:
            other: Another BalancedTernary instance.

        Returns:
            The product as a new BalancedTernary.

        Raises:
            TypeError: If other is not a BalancedTernary.
        """
        if not isinstance(other, BalancedTernary):
            return NotImplemented
        return BalancedTernary(_mul_digits(list(self._digits), list(other._digits)))

    def __eq__(self, other: object) -> bool:
        """Test equality.

        Args:
            other: Any object.

        Returns:
            True if other is a BalancedTernary with the same digit list.
        """
        if not isinstance(other, BalancedTernary):
            return NotImplemented
        return self._digits == other._digits

    def __hash__(self) -> int:
        """Return a hash based on the normalized digit tuple.

        Returns:
            Hash of the internal digit tuple.
        """
        return hash(tuple(self._digits))

    def __repr__(self) -> str:
        """Return an unambiguous representation.

        Returns:
            String of the form BalancedTernary.from_str('...').
        """
        return f"BalancedTernary.from_str({self.to_str()!r})"

    def __str__(self) -> str:
        """Return the canonical T-notation string.

        Returns:
            T-notation string, same as to_str().
        """
        return self.to_str()
