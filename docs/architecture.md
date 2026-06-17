# Architecture: balanced-ternary

## Representation

A `BalancedTernary` value is stored as `_digits: list[int]` in **least-significant-first**
order. Each element is exactly -1, 0, or 1.

**Canonical (normalized) form**: no trailing zeros (high-order zero digits) except
that zero itself is `[0]`. Normalization is applied after every operation.

Example: the integer 5 is stored as `[-1, -1, 1]`, which in most-significant-first
T-notation reads "1TT": 1*9 + (-1)*3 + (-1)*1 = 5.

## T-notation

In T-notation, the digit -1 is written as `T` (or lowercase `t` on input).

| Integer | Balanced ternary | T-notation |
|---------|-----------------|------------|
| 5       | 1, -1, -1       | 1TT        |
| -7      | -1, 1, -1       | T1T        |
| 2       | -1, 1           | 1T         |
| 0       | 0               | 0          |
| 1       | 1               | 1          |

The string is always most-significant-first for readability. Internally the list is
least-significant-first for convenient index-aligned arithmetic.

## Conversion from int

Repeated balanced remainder extraction:

```
n != 0:
    r = n mod 3   (Python: r = n % 3, result in {0, 1, 2, -2, -1} by Python mod rules)
    if r == 2:  r = -1
    if r == -2: r = 1
    append r to digits
    n = (n - r) // 3
```

This terminates because |n| strictly decreases each iteration.

## Digit-level addition

The carry table covers all possible column sums when adding two balanced ternary digits
plus a carry from {-1, 0, 1}. The column sum s = d1 + d2 + carry ranges from -3 to 3:

| s  | result digit | carry out |
|----|-------------|-----------|
| -3 | 0           | -1        |
| -2 | 1           | -1        |
| -1 | -1          | 0         |
| 0  | 0           | 0         |
| 1  | 1           | 0         |
| 2  | -1          | 1         |
| 3  | 0           | 1         |

Addition scans from least to most significant position, applying the table at each
position, and appends a final carry digit if non-zero.

## Negation

Negation in balanced ternary is exact: flip the sign of every digit (-1 <-> 1,
0 stays 0). No carry is needed. This is a unique property of balanced ternary that
binary does not share.

## Subtraction

Subtraction is `self + (-other)`. The negation is computed first (exact, no carry),
then digit-level addition is applied.

## Digit-level multiplication

For each digit `b_i` of the second operand (at position i):

1. Skip if `b_i == 0`.
2. Compute the partial product: `[i zeros] + [da * b_i for da in a]`. Since b_i is
   in {-1, 1}, each partial digit is in {-1, 0, 1} -- no carry needed within a
   partial product.
3. Accumulate the partial product into a running sum using digit-level addition.

The final sum is the product. This mirrors the standard long-multiplication algorithm
but in balanced ternary rather than binary or decimal.

## Immutability

`BalancedTernary` is immutable. All arithmetic returns new instances. Internal lists
are copied before mutation. `__slots__` is used to prevent attribute addition.

## Module layout

```
src/balanced_ternary/
    __init__.py    re-exports BalancedTernary and __version__
    _core.py       BalancedTernary class and all digit-level functions
    py.typed       PEP 561 marker (empty file)
```

All digit-level functions (`_add_digits`, `_mul_digits`, `_negate_digits`,
`_normalize`) are module-private (underscore prefix) and not part of the public API.
