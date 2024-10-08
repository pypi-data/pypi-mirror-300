# SPDX-License-Identifier: MIT

import re
from pprint import pprint  # noqa E401
import sys  # noqa E401

"""Utilities to smooth out language rules.

``talkgooder`` attempts to smooth out grammar, punctuation, and number-related corner cases when
formatting text for human consumption. It is intended for applications where you know there's a
noun and are trying to generate text, but you don't know much about it.
"""


def plural(
    text: str,
    number: int | float,
    language="en-US",
    addl_same=[],
    addl_special_s=[],
    addl_irregular={},
    caps_mode=0,
) -> str:
    """Determine the plural of a noun depending upon quantity.

    Given a quantity of nouns, return the most likely plural form. Language is complicated and
    pluralization rules are not always consistent, so this function supports user-supplied rules
    to accommodate exceptions specific to the situation.

    **Supported locales:**

    * ``en-US``: American English

    Args:
        text (str):
            The noun to convert.
        number (int or float):
            The quantity of nouns.
        language (str):
            Which language rules to apply, specified by locale (default: ``en-US``).
        addl_same (list):
            Additional words where the singular and plural are the same.
        addl_special_s (list):
            Additional words that always end in s for odd reasons (e.g., ``["piano","hello",...]``).
        addl_irregular (dict):
            Additional pairs of irregular plural nouns (e.g., ``{"mouse": "mice", "person":
            "people", ...}``).
        caps_mode (int):

            * ``0``: Attempt to infer whether suffix is lower or upper case (default).
            * ``1``: Force suffix to be upper case.
            * ``2``: Force suffix to be lower case.

    Returns:
        String:
            The plural of the provided noun.

    Raises:
        TypeError: Text must be a string.
        ValueError: Language must be a supported locale.
    """

    # Thanks to Grammarly for publishing a guideline that helped inspire these rules:
    # https://www.grammarly.com/blog/irregular-plural-nouns/

    # Make sure something reasonable was supplied
    if not isinstance(number, (int, float)):
        raise TypeError("Number must be an int or a float")

    if language.lower() == "en-us":

        # Same singular as plural, can be extended via addl_same parameter
        en_us_same = [
            "aircraft",
            "buffalo",
            "deer",
            "fish",
            "goose",
            "hovercraft",
            "moose",
            "salmon",
            "sheep",
            "shrimp",
            "spacecraft",
            "trout",
            "watercraft",
        ] + addl_same

        # Doesn't follow other rules, plural is always s, can be extended via addl_special_s
        en_us_special_s = [
            "cello",
            "hello",
            "photo",
            "piano",
            "proof",
            "roof",
            "spoof",
            "zero",
        ] + addl_special_s

        # Irregular plurals where there's no rule, it just is, can be extended via addl_irregular
        en_us_irregular = dict(
            list(
                {
                    "child": "children",
                    "criterion": "criteria",
                    "die": "dice",
                    "louse": "lice",
                    "man": "men",
                    "mouse": "mice",
                    "ox": "oxen",
                    "person": "people",
                    "phenomenon": "phenomena",
                    "tooth": "teeth",
                    "woman": "women",
                }.items()
            )
            + list(addl_irregular.items())
        )

        # Consonent before y pattern
        en_us_ies_pattern = re.compile(
            r"[b-df-hj-np-tv-z]+y$",
            re.IGNORECASE,
        )

        # If the entire word is upper case or caps_mode is 1, capitalize it
        if caps_mode == 2:
            casing = "lower"
        elif text.isupper() or caps_mode == 1:
            casing = "upper"
        else:
            casing = "lower"

        if casing == "upper":
            i = "I"
            a = "A"
            ices = "ICES"
            es = "ES"
            ies = "IES"
            ves = "VES"
            s = "S"

        else:
            i = "i"
            a = "a"
            ices = "ices"
            es = "es"
            ies = "ies"
            ves = "ves"
            s = "s"

        # If the number is an integer that is exactly 1, nothing to do
        if isinstance(number, int) and number == 1:
            return text

        # If the word is the same whether singular or plural, nothing to do
        if text.lower() in en_us_same:
            return text

        # Some words follow no rules whatsoever
        for item in en_us_irregular.keys():
            if text.lower().endswith(item.lower()):
                if text.isupper():
                    return en_us_irregular[item].upper()
                else:
                    return en_us_irregular[item]

        if text.lower() in en_us_special_s:
            # Certain words always end with s for Reasons
            return "%s%s" % (text, s)

        if text.lower().endswith("us"):
            # Words that end in "us" change to "i" when plural
            return "%s%s" % (text[:-2], i)

        if text.lower().endswith("um"):
            # Words that end in "um" change to "a" when plural
            return "%s%s" % (text[:-2], a)

        if text.lower().endswith(("ix", "ex")):
            # Words that end in "ix" or "ex" change to "ices" when plural
            return "%s%s" % (text[:-2], ices)

        if text.lower().endswith(("o", "s", "x", "z", "ch", "sh", "is")):
            # Words that end in "o", "s", "x", "z", "ch", "sh", and "is" change to "es" when plural
            return "%s%s" % (text, es)

        if text.lower().endswith(("f", "fe")):
            # Words that end in "f" or "fe" end in "ves" when plural
            return "%s%s" % (text[:-1], ves)

        if en_us_ies_pattern.findall(text):
            # Words that end in a consonant then "y" end in "ies" when plural
            return "%s%s" % (text[:-1], ies)

        # Remaining words end in "s" when plural
        return "%s%s" % (text, s)

    else:
        raise ValueError("Language must be a supported locale.")


def possessive(
    text: str,
    language="en-US",
    caps_mode=0,
) -> str:
    """Convert a noun to its possessive, because apostrophes can be hard.

    **Supported locales:**

    * ``en-US``: American English

    Args:
        text (str):
            A noun to be made possessive.

        language (str):
            Which language rules to apply (default ``en-US``).

        caps_mode (int):

            * ``0``: Attempt to infer whether suffix is lower or upper case (default).
            * ``1``: Force suffix to be upper case.
            * ``2``: Force suffix to be lower case.

    Returns:
        String:
            The possessive of the provided string.

    Raises:
        TypeError: Text must be a string.
        ValueError: Language must be a supported locale.
    """

    if not isinstance(text, str):
        raise TypeError("Text must be a string")

    if language.lower() == "en-us":
        if text.endswith("s"):
            # When a noun ends in "s", just add an apostrophe
            return "%s'" % text

        else:
            if caps_mode == 2:
                # Force lower case
                return "%s's" % text
            elif text.isupper() or caps_mode == 1:
                # Force upper case or detect upper case
                return "%s'S" % text
                # Default is lower
            else:
                return "%s's" % text

    else:
        raise ValueError("Language must be a supported locale.")


def num2word(
    number: int,
    language="en-US",
) -> str:
    """Determine if an integer should be expanded to a word (per the APA style manual).

    The APA style manual specifies integers between 1 and 9 should be written out as a word.
    Everything else should be represented as digits.

    **Supported locales:**

    * ``en-US``: American English

    Args:
        number (int):
            An integer.
        language (str):
            Which language rules to apply (default ``en-US``).

    Returns:
        String:
            The word or string-formatted number, as appropriate.

    Raises:
        TypeError: Number must be an int.
        ValueError: Language must be a supported locale.
    """

    # Make sure something reasonable was supplied
    if not isinstance(number, int):
        raise TypeError("Number must be an int.")

    # Per APA style guide, only 1-9 should be expanded
    if number < 1 or number > 9:
        return str(number)

    if language.lower() == "en-us":
        numbers = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
    else:
        raise ValueError("Language must be a supported locale.")

    return numbers[number - 1]


def isAre(
    number: int | float,
    language="en-US",
) -> str:
    """Given a quanity, determine if article should be ``is`` or ``are``.

    Given a quantity of nouns or noun-equivalents, determine whether the article should be
    ``is`` or ``are``. For example, "there is one cat," and "there are two cats."

    **Supported locales:**

    * ``en-US``: American English

    Args:
        number (int | float):
            Quantity of items.
        language (str):
            Which language rules to apply, specified by locale (default ``en-US``).

    Returns:
        String:
            ``is`` or ``are``, as appropriate.

    Raises:
        TypeError: number must be an int or float.
        ValueError: language must be a supported locale.
    """

    if not isinstance(number, (int, float)):
        raise TypeError("Number must be an int or a float.")

    if language.lower() == "en-us":
        # Anything other than integer 1 (even 1.0) uses "are"
        if number == 1 and isinstance(number, int):
            return "is"
        else:
            return "are"

    else:
        raise ValueError("Language must be a supported locale.")


def wasWere(
    number: int | float,
    language="en-US",
) -> str:
    """Given a quanity, determine if article should be ``ws`` or ``were``.

    Given a quantity of nouns or noun-equivalents, determine whether the article should be
    ``was`` or ``were``. For example, "there was one cat," and "there were two cats."

    **Supported locales:**

    * ``en-US``: American English

    Args:
        number (int | float):
            Quantity of items.
        language (str):
            Which language rules to apply, specified by locale (default ``en-US``).

    Returns:
        String:
            ``was`` or ``were``, as appropriate.

    Raises:
        TypeError: number must be an int or float.
        ValueError: language must be a supported locale.
    """

    if not isinstance(number, (int, float)):
        raise TypeError("Number must be an int or a float.")

    if language.lower() == "en-us":
        # Anything other than integer 1 (even 1.0) uses "were"
        if number == 1 and isinstance(number, int):
            return "was"
        else:
            return "were"

    else:
        raise ValueError("Language must be a supported locale.")


def aAn(
    noun: str | int | float,
    language="en-US",
) -> str:
    """Given a noun or noun-equivalent, determine whether the article is ``a`` or ``an``.

    Nouns and noun-equivalents with a soft vowel beginning generally use ``an``, and everything
    else uses ``a``.

    **Supported locales:**

    * ``en-US``: American English

    Args:
        noun (str | int | float):
            A noun or noun-equivalent, as a word or a number.

        language (str):
            Which language rules to apply, specified by locale (default ``en-US``).

    Returns:
        String:
            ``a`` or ``an``, as appropriate.

    Raises:
        TypeError: Noun must be a string, int, or float.
        ValueError: Language must be a supported locale.
    """

    if not isinstance(noun, (str, int, float)):
        raise TypeError("Noun must be a string, int, or float.")

    if language.lower() == "en-us":

        # Vowels, numbers that start with 8, and 18 use the "an" article
        if (
            str(noun).lower().startswith(("a", "e", "i", "o", "u", "8", "18."))
            or str(noun) == "18"
        ):
            return "an"
        else:
            return "a"
    else:
        raise ValueError("Language must be a supported locale.")
