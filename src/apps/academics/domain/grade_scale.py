from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LetterRange:
    """
    Represents a letter grade and its numeric inclusive range.
    """
    letter: str
    min_value: int
    max_value: int


# Full scale (as described in the challenge)
GRADE_SCALE: tuple[LetterRange, ...] = (
    LetterRange("A+", 97, 100),
    LetterRange("A", 93, 96),
    LetterRange("A-", 90, 92),
    LetterRange("B+", 87, 89),
    LetterRange("B", 83, 86),
    LetterRange("B-", 80, 82),
    LetterRange("C+", 77, 79),
    LetterRange("C", 73, 76),
    LetterRange("C-", 70, 72),
    LetterRange("D", 60, 69),
    LetterRange("F", 0, 59),
)


def letter_to_numeric_max(letter: str) -> int:
    """
    Convert a letter grade to the numeric MAX value of its interval.

    Example:
      "A"  -> 96
      "A+" -> 100
      "F"  -> 59
    """
    normalized = letter.strip().upper()
    for r in GRADE_SCALE:
        if r.letter == normalized:
            return r.max_value
    raise ValueError(f"Unknown letter grade: {letter!r}")


def numeric_to_letter(value: int) -> str:
    """
    Convert a numeric grade (0..100) to its corresponding letter grade.
    """
    if not isinstance(value, int):
        raise TypeError("Numeric grade must be an integer.")
    if value < 0 or value > 100:
        raise ValueError("Numeric grade must be between 0 and 100 (inclusive).")

    for r in GRADE_SCALE:
        if r.min_value <= value <= r.max_value:
            return r.letter

    # Defensive (should never happen if scale covers 0..100)
    raise ValueError(f"Numeric grade {value} does not match any letter range.")
