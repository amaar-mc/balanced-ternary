# balanced-ternary

Pure-Python balanced ternary number type: T-notation, conversions, and digit-level
arithmetic (digits -1, 0, 1). Zero runtime dependencies.

## Commands

- Create env and install: `uv venv && uv pip install -e ".[dev]"`
- Test: `uv run pytest -q`
- Lint: `uv run ruff check .` (format with `uv run ruff format .`)
- Types: `uv run mypy src`
- Build: `uv build` (then `uv run --with twine twine check dist/*` before publishing)

## Architecture

`src/balanced_ternary/`:
- `_core.py`: `BalancedTernary` class, `_add_digits`, `_mul_digits`, `_negate_digits`,
  `_normalize`, `_CARRY_TABLE`.
- `__init__.py`: public surface -- re-exports `BalancedTernary` and `__version__`.
- `py.typed`: PEP 561 marker.

See `docs/architecture.md` for the representation, carry table, and multiplication algorithm.

## Conventions

- Digits stored as `list[int]` in least-significant-first order, each in {-1, 0, 1}.
- Normalized form: no trailing zeros (high-order zeros), except `[0]` for zero.
- T-notation strings are most-significant-first; T (or t) represents -1.
- No default parameter values; all parameters explicit.
- Pure functions for the digit-level operations; `BalancedTernary` is immutable.
- Strict typing; all public and private functions annotated.

## Testing rules

- Golden values: from_int(5)=="1TT", from_int(-7)=="T1T", from_int(2)=="1T",
  from_int(0)=="0", from_int(1)=="1".
- Round-trip tests over -1000..1000 for int and over canonical strings.
- Hypothesis property tests validate digit-level arithmetic against int oracle.
- Error cases: empty string and invalid characters raise ValueError with clear messages.
- Bug fixes start with a failing test.

## Release

- Semantic versioning; update CHANGELOG.md and `__version__`.
- Gates: `uv run pytest && uv run ruff check . && uv run mypy src && uv build && uv run --with twine twine check dist/*`.
- Do NOT publish to PyPI (pending quota reset). Tag vX.Y.Z and GitHub release.

## Style

- No em dash characters in docs, comments, or commit messages.
- Comments explain non-obvious reasoning only.
- No TODO or FIXME in code.
