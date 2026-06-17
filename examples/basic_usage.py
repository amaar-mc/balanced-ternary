"""Basic usage examples for balanced-ternary."""

from balanced_ternary import BalancedTernary


def main() -> None:
    # Convert from int to balanced ternary
    a = BalancedTernary.from_int(5)
    print(f"5 in balanced ternary: {a.to_str()}")   # "1TT"

    b = BalancedTernary.from_int(-7)
    print(f"-7 in balanced ternary: {b.to_str()}")  # "T1T"

    # Parse T-notation strings
    c = BalancedTernary.from_str("1T")
    print(f"'1T' as int: {c.to_int()}")            # 2

    # Digit-level arithmetic
    x = BalancedTernary.from_int(5)
    y = BalancedTernary.from_int(3)

    print(f"5 + 3 = {(x + y).to_int()}")           # 8
    print(f"5 - 3 = {(x - y).to_int()}")           # 2
    print(f"5 * 3 = {(x * y).to_int()}")           # 15

    # Negation is exact: flip sign of every digit, no carry needed
    print(f"-5 in balanced ternary: {(-x).to_str()}")  # "T11"

    # Lowercase t is accepted for -1
    d = BalancedTernary.from_str("1t")
    print(f"'1t' as int: {d.to_int()}")            # 2
    print(f"'1t' canonical: {d.to_str()}")          # "1T"

    # Equality and hashing
    p = BalancedTernary.from_int(42)
    q = BalancedTernary.from_str("1TT0")
    print(f"from_int(42) == from_str('1TT0'): {p == q}")  # True

    # Usable as dict keys
    values = {BalancedTernary.from_int(n): n for n in range(-3, 4)}
    print(f"Dict lookup: {values[BalancedTernary.from_int(2)]}")  # 2

    # repr
    print(repr(BalancedTernary.from_int(5)))  # BalancedTernary.from_str('1TT')


if __name__ == "__main__":
    main()
