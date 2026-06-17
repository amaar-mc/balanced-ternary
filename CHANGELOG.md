# Changelog

All notable changes to balanced-ternary are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-17

### Added

- `BalancedTernary` class with digits from {-1, 0, 1} and T-notation strings.
- `from_int(value)` classmethod for conversion from Python int.
- `from_str(text)` classmethod for parsing T-notation strings (T or t = -1).
- `to_int()` method returning the integer value.
- `to_str()` method returning the canonical T-notation string.
- Digit-level addition with balanced-ternary carry logic.
- Digit-level multiplication via digit-by-digit partial products.
- Exact negation (digit sign flip, no carry needed).
- Subtraction implemented as addition of the negation.
- `__eq__` and `__hash__` for use as dict keys and in sets.
- `__repr__` and `__str__` using T-notation.
- `py.typed` marker for PEP 561 compliance.
- Full type annotations, mypy strict mode clean.
- pytest + Hypothesis test suite covering golden values, round-trips, and
  arithmetic oracle verification.
