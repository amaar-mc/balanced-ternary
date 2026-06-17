# Project Charter: balanced-ternary

## Mission

Provide a correct, well-tested, pure-Python implementation of balanced ternary arithmetic
as a typed library with zero runtime dependencies.

## Scope

In scope:

- The `BalancedTernary` type with T-notation string parsing and formatting
- Digit-level addition and multiplication using balanced ternary carry logic
- Exact negation (digit sign flip)
- Subtraction as addition of the negation
- Equality, hashing, and standard Python dunder methods
- Full mypy strict type checking
- pytest + Hypothesis test suite with int oracle validation

Out of scope:

- Floating-point balanced ternary
- Arbitrary precision beyond Python int
- Conversion to/from other bases (binary, decimal string, etc.) beyond int
- Hardware or SIMD acceleration

## Audience

Mathematicians, educators, and developers interested in non-standard numeral systems.
The library is intentionally simple; the interesting depth is in the digit-level carry
arithmetic and the T-notation.

## Quality bar

- All five golden values must pass
- Round-trip correctness over integers -1000..1000
- Hypothesis property tests validate digit-level arithmetic against Python int for at
  least 500 examples each for add, sub, mul and 300 for neg
- mypy strict, ruff clean, zero runtime dependencies
- PyPI distribution pending; GitHub release is the primary delivery vehicle

## Versioning

Semantic versioning. The public API is `BalancedTernary` plus `from_int`, `from_str`,
`to_int`, `to_str`, and the operator overloads. Internal functions prefixed with `_`
are not part of the public API.
