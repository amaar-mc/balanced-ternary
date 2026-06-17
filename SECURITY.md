# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability in balanced-ternary, please do not open a
public GitHub issue. Instead, contact the maintainer directly via the email address
listed on the GitHub profile.

Please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Any potential impact you have identified

You will receive a response within 7 days. If the vulnerability is confirmed, a patch
will be released as soon as reasonably possible and a public advisory will be issued.

## Scope

balanced-ternary is a pure-Python arithmetic library with zero runtime dependencies.
It does not perform network requests, file I/O, or execute external processes.
Security issues most likely to apply are:

- Integer overflow or unbounded resource consumption on very large inputs
- Incorrect arithmetic results that could affect downstream security-sensitive calculations
