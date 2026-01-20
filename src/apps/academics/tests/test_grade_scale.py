import pytest

from apps.academics.domain.grade_scale import letter_to_numeric_max, numeric_to_letter


@pytest.mark.parametrize(
    "letter,expected",
    [
        ("A+", 100),
        ("A", 96),
        ("A-", 92),
        ("B+", 89),
        ("B", 86),
        ("B-", 82),
        ("C+", 79),
        ("C", 76),
        ("C-", 72),
        ("D", 69),
        ("F", 59),
        (" a ", 96),  # normalization check
    ],
)
def test_letter_to_numeric_max(letter, expected):
    assert letter_to_numeric_max(letter) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (100, "A+"),
        (97, "A+"),
        (96, "A"),
        (93, "A"),
        (92, "A-"),
        (90, "A-"),
        (89, "B+"),
        (60, "D"),
        (59, "F"),
        (0, "F"),
    ],
)
def test_numeric_to_letter(value, expected):
    assert numeric_to_letter(value) == expected


def test_letter_to_numeric_max_raises_on_unknown():
    with pytest.raises(ValueError):
        letter_to_numeric_max("Z")


def test_numeric_to_letter_raises_on_out_of_range():
    with pytest.raises(ValueError):
        numeric_to_letter(101)
