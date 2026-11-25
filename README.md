# password-generator

A small command-line tool that generates random passwords — one per line,
copy-friendly, no decoration. Randomness comes from Python's
`random.SystemRandom` (the OS cryptographically strong random source).
Every enabled character class is guaranteed to appear at least once in
each password.

## Install

```bash
pip install -e .
```

## Usage

```bash
# One 16-character password (the default)
python -m password_gen.cli

# A 24-character password, no punctuation
python -m password_gen.cli --length 24 --no-symbols

# Five 12-character passwords, letters and digits only, no look-alikes
python -m password_gen.cli --length 12 --count 5 --no-symbols --exclude-ambiguous

# Save passwords to a file instead of printing them
python -m password_gen.cli --count 10 --output passwords.txt
```

## Options

| Option | What it does |
| --- | --- |
| `--length N` | Password length (default 16). Must fit at least one character from every enabled class. |
| `--count N` | How many passwords to generate (default 1). |
| `--no-symbols` | Leave punctuation out. |
| `--no-digits` | Leave digits out. |
| `--no-uppercase` | Leave A–Z out. |
| `--no-lowercase` | Leave a–z out. |
| `--exclude-ambiguous` | Drop look-alike characters (`I`, `l`, `1`, `O`, `0`). |
| `--output FILE` | Write passwords to FILE instead of stdout. |

## Tests

```bash
python -m pytest
```

## Notes

- Passwords are generated locally with `random.SystemRandom` (the OS
  CSPRNG); nothing is sent anywhere.
- The repository contains no real passwords — only test fixtures and
  example commands.
