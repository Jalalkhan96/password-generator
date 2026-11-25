"""Tests for password-generator."""

import random
import string

import pytest

from password_gen.generator import (
    AMBIGUOUS,
    SYMBOLS,
    generate_password,
    generate_passwords,
)
from password_gen.cli import main


def test_default_length_is_16():
    assert len(generate_password(rng=random.Random(1))) == 16


def test_custom_length_respected():
    for length in (8, 24, 32):
        assert len(generate_password(length=length,
                                     rng=random.Random(length))) == length


def test_seeded_rng_is_deterministic():
    first = generate_password(rng=random.Random(7))
    second = generate_password(rng=random.Random(7))
    assert first == second


def test_different_seeds_differ():
    assert (generate_password(length=32, rng=random.Random(1))
            != generate_password(length=32, rng=random.Random(2)))


def test_each_enabled_class_present():
    password = generate_password(length=16, rng=random.Random(3))
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in SYMBOLS for c in password)


def test_no_symbols():
    password = generate_password(length=20, use_symbols=False,
                                 rng=random.Random(4))
    assert not any(c in SYMBOLS for c in password)


def test_no_digits():
    password = generate_password(length=20, use_digits=False,
                                 rng=random.Random(5))
    assert not any(c.isdigit() for c in password)


def test_no_uppercase_and_no_lowercase():
    password = generate_password(length=12, use_uppercase=False,
                                 use_lowercase=False, use_symbols=False,
                                 rng=random.Random(6))
    assert password.isdigit()


def test_exclude_ambiguous():
    password = generate_password(length=40, exclude_ambiguous=True,
                                 rng=random.Random(8))
    assert not any(c in AMBIGUOUS for c in password)


def test_length_too_short_for_classes():
    with pytest.raises(ValueError):
        generate_password(length=3, rng=random.Random(9))


def test_all_classes_disabled():
    with pytest.raises(ValueError):
        generate_password(use_symbols=False, use_digits=False,
                          use_uppercase=False, use_lowercase=False,
                          rng=random.Random(10))


def test_generate_passwords_count():
    passwords = generate_passwords(count=5, length=10,
                                   rng=random.Random(11))
    assert len(passwords) == 5
    assert all(len(p) == 10 for p in passwords)


def test_generate_passwords_count_zero_rejected():
    with pytest.raises(ValueError):
        generate_passwords(count=0, rng=random.Random(12))


def test_cli_prints_one_password_per_line(capsys):
    assert main(["--length", "12", "--count", "3"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 3
    assert all(len(line) == 12 for line in lines)


def test_cli_no_digits_flag(capsys):
    assert main(["--length", "20", "--no-digits"]) == 0
    assert not any(c.isdigit()
                   for c in capsys.readouterr().out.strip())


def test_cli_invalid_length_exits_2(capsys):
    assert main(["--length", "2"]) == 2
    assert "error:" in capsys.readouterr().err


def test_cli_output_file(tmp_path):
    target = tmp_path / "passwords.txt"
    assert main(["--length", "10", "--count", "2",
                 "--output", str(target)]) == 0
    lines = target.read_text().splitlines()
    assert len(lines) == 2
    assert all(len(line) == 10 for line in lines)
