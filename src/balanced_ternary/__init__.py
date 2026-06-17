"""balanced_ternary: A pure-Python balanced ternary number type.

Provides the BalancedTernary class for working with balanced ternary integers
using digits {-1, 0, 1} and T-notation strings. Arithmetic is implemented at
the digit level with balanced-ternary carry logic.

Example:
    >>> from balanced_ternary import BalancedTernary
    >>> a = BalancedTernary.from_int(5)
    >>> a.to_str()
    '1TT'
    >>> b = BalancedTernary.from_str("1T")
    >>> b.to_int()
    2
    >>> (a + b).to_int()
    7
"""

from balanced_ternary._core import BalancedTernary

__all__ = ["BalancedTernary"]
__version__ = "0.2.0"
