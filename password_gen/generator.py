"""Password generator helpers.

Generates random passwords with :class:`random.SystemRandom` (the OS
cryptographically strong random source). Every enabled character class is
guaranteed to appear at least once in the generated password.
"""

import random
import string

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"

# Characters that are easy to confuse when read aloud or typed from a
# screenshot: capital i, lowercase L, digit one, capital O, digit zero.
AMBIGUOUS = "Il1O0"


def _remove_ambiguous(chars):
    """Return *chars* with every ambiguous character removed."""
    return "".join(c for c in chars if c not in AMBIGUOUS)


def generate_password(length=16, use_symbols=True, use_digits=True,
                      use_uppercase=True, use_lowercase=True,
                      exclude_ambiguous=False, rng=None):
    """Generate one random password.

    Args:
        length: Password length. Must be at least the number of enabled
            character classes (each class contributes at least one char).
        use_symbols: Include punctuation characters.
        use_digits: Include digits 0-9.
        use_uppercase: Include A-Z.
        use_lowercase: Include a-z.
        exclude_ambiguous: Drop characters that look alike (I, l, 1, O, 0).
        rng: Optional random source with ``choice`` and ``shuffle`` methods
            (defaults to ``random.SystemRandom``, which draws from the OS
            CSPRNG). Tests pass a seeded :class:`random.Random` for
            deterministic output.

    Returns:
        The generated password string.

    Raises:
        ValueError: If no character class is enabled, or *length* is too
            short to hold one character from every enabled class.
    """
    if rng is None:
        rng = random.SystemRandom()

    pools = []
    if use_lowercase:
        pools.append(_remove_ambiguous(LOWERCASE) if exclude_ambiguous
                     else LOWERCASE)
    if use_uppercase:
        pools.append(_remove_ambiguous(UPPERCASE) if exclude_ambiguous
                     else UPPERCASE)
    if use_digits:
        pools.append(_remove_ambiguous(DIGITS) if exclude_ambiguous
                     else DIGITS)
    if use_symbols:
        pools.append(SYMBOLS)

    if not pools:
        raise ValueError("at least one character class must be enabled")
    if length < len(pools):
        raise ValueError(
            "length %d is too short for %d enabled character classes"
            % (length, len(pools)))
    if length < 1:
        raise ValueError("length must be at least 1")

    # One guaranteed character from each enabled class, then fill the rest
    # from the combined pool and shuffle so the classes are not in order.
    chars = [rng.choice(pool) for pool in pools]
    combined = "".join(pools)
    chars.extend(rng.choice(combined) for _ in range(length - len(pools)))
    rng.shuffle(chars)
    return "".join(chars)


def generate_passwords(count=1, **kwargs):
    """Generate *count* passwords with the same options.

    Raises:
        ValueError: If *count* is less than 1.
    """
    if count < 1:
        raise ValueError("count must be at least 1")
    return [generate_password(**kwargs) for _ in range(count)]
