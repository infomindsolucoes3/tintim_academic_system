from __future__ import annotations

from django.db import transaction

from apps.academics.domain.exceptions import (
    InvalidGradeInputError,
    InvalidLetterGradeError,
    NoGradesRecordedError,
    StudentNotEnrolledError,
)
from apps.academics.domain.grade_scale import letter_to_numeric_max, numeric_to_letter
from apps.academics.domain.models import Enrollment, Grade


def _round_half_up(x: float) -> int:
    """
    Round halves away from zero (e.g., 80.5 -> 81).

    Python's built-in round() uses bankers rounding, which is not desired here.
    """
    if x >= 0:
        return int(x + 0.5)
    return int(x - 0.5)


def _get_enrollment_or_raise(*, student_id, course_id) -> Enrollment:
    enrollment = Enrollment.objects.filter(student_id=student_id, course_id=course_id).first()
    if enrollment is None:
        raise StudentNotEnrolledError(student_id=student_id, course_id=course_id)
    return enrollment


@transaction.atomic
def record_grade(
    *,
    student_id,
    course_id,
    numeric: int | None = None,
    letter: str | None = None,
) -> Grade:
    """
    Record a grade for a student in a course.

    Rules:
    - Student must be enrolled in the course.
    - Grade must be provided as either numeric (0..100) OR letter.
    - Providing both or neither results in a domain error.
    - Letter grades are converted to the numeric MAX of the letter interval.
    - Grades are historical records (append-only).
    """
    enrollment = _get_enrollment_or_raise(student_id=student_id, course_id=course_id)

    has_numeric = numeric is not None
    has_letter = letter is not None and str(letter).strip() != ""

    if has_numeric == has_letter:
        raise InvalidGradeInputError(
            "Grade must be provided as exactly one of: numeric (0..100) OR letter."
        )

    if has_numeric:
        if not isinstance(numeric, int):
            raise InvalidGradeInputError("Numeric grade must be an integer.")
        if numeric < 0 or numeric > 100:
            raise InvalidGradeInputError("Numeric grade must be between 0 and 100 (inclusive).")
        numeric_value = numeric
    else:
        try:
            numeric_value = letter_to_numeric_max(str(letter))
        except ValueError:
            raise InvalidLetterGradeError(letter=str(letter))

    return Grade.objects.create(enrollment=enrollment, numeric_value=numeric_value)


def get_numeric_grades(*, student_id, course_id) -> list[int]:
    enrollment = _get_enrollment_or_raise(student_id=student_id, course_id=course_id)
    return list(
        Grade.objects.filter(enrollment=enrollment)
        .order_by("created_at")
        .values_list("numeric_value", flat=True)
    )


def get_letter_grades(*, student_id, course_id) -> list[str]:
    values = get_numeric_grades(student_id=student_id, course_id=course_id)
    return [numeric_to_letter(v) for v in values]


def calculate_numeric_average(*, student_id, course_id) -> int:
    values = get_numeric_grades(student_id=student_id, course_id=course_id)
    if not values:
        raise NoGradesRecordedError(student_id=student_id, course_id=course_id)

    avg = sum(values) / len(values)
    return _round_half_up(avg)


def calculate_letter_average(*, student_id, course_id) -> str:
    avg = calculate_numeric_average(student_id=student_id, course_id=course_id)
    return numeric_to_letter(avg)
