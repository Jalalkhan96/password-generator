"""Command-line interface for password-generator.

Prints one password per line (copy-friendly: no decoration, no labels),
or writes them to a file with --output.
"""

import argparse
import sys

from .generator import generate_passwords


def build_parser():
    parser = argparse.ArgumentParser(
        prog="password-generator",
        description="Generate random passwords (one per line).")
    parser.add_argument("--length", type=int, default=16,
                        help="password length (default: 16)")
    parser.add_argument("--count", type=int, default=1,
                        help="how many passwords to generate (default: 1)")
    parser.add_argument("--no-symbols", action="store_true",
                        help="leave punctuation out of the password")
    parser.add_argument("--no-digits", action="store_true",
                        help="leave digits out of the password")
    parser.add_argument("--no-uppercase", action="store_true",
                        help="leave uppercase letters out of the password")
    parser.add_argument("--no-lowercase", action="store_true",
                        help="leave lowercase letters out of the password")
    parser.add_argument("--exclude-ambiguous", action="store_true",
                        help="drop look-alike characters (I, l, 1, O, 0)")
    parser.add_argument("--output", type=argparse.FileType("w"),
                        default=sys.stdout,
                        help="write passwords to FILE instead of stdout")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        passwords = generate_passwords(
            count=args.count,
            length=args.length,
            use_symbols=not args.no_symbols,
            use_digits=not args.no_digits,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            exclude_ambiguous=args.exclude_ambiguous,
        )
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    out = args.output
    for password in passwords:
        out.write(password + "\n")
    if out is not sys.stdout:
        out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
