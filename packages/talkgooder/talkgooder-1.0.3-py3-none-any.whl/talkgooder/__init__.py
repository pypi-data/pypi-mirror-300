"""
talkGooder
~~~~~~~~~~

`talkgooder` attempts to smooth out grammar, punctuation, and number-related corner cases when
formatting text for human consumption.

:copyright: (c) 2024 by Brian Warner
:license: MIT, see LICENSE.md for more details.
"""

# Porcelain functions
from .talkgooder import plural, possessive, num2word, isAre, aAn  # NOQA F401
