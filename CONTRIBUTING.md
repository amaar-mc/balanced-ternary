# Contributing to balanced-ternary

Thank you for taking the time to contribute.

## Getting started

1. Fork the repository on GitHub.
2. Clone your fork and install the dev dependencies:

   ```
   git clone https://github.com/<your-username>/balanced-ternary
   cd balanced-ternary
   uv pip install -e ".[dev]"
   ```

3. Create a branch for your change:

   ```
   git checkout -b feat/your-feature
   ```

## Development workflow

Run the full check suite before opening a pull request:

```
uv run pytest -q          # tests
uv run ruff check .       # linting
uv run mypy src           # type checking
```

All three must pass with zero errors.

## Code style

- Python 3.10+ type annotations on all public and private functions.
- Black-compatible line length (88 characters).
- Google-style docstrings.
- No runtime dependencies -- the package must stay dependency-free.
- No TODO or FIXME comments -- implement the thing or leave it out.

## Submitting a pull request

- Keep changes focused. One logical change per PR.
- Update CHANGELOG.md under an `[Unreleased]` section.
- Add or update tests to cover the change. Aim for 90%+ coverage.
- The CI pipeline must pass.

## Reporting issues

Use the GitHub issue tracker. For security vulnerabilities, see SECURITY.md.

## License

By contributing you agree that your contributions will be licensed under the
MIT License that covers this project.
