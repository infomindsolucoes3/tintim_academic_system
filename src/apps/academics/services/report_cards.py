from __future__ import annotations

from dataclasses import dataclass

from apps.academics.domain.grade_scale import numeric_to_letter
from apps.academics.domain.models import Enrollment, Grade
from apps.academics.services.grades import _round_half_up


@dataclass(frozen=True)
class CourseReport:
    """
    Consolidated view of a student's performance in a given course.
    """
    course_id: object
    course_name: str
    numeric_grades: list[int]
    numeric_average: int
    letter_average: str


@dataclass(frozen=True)
class StudentReportCard:
    """
    Consolidated report card for a student across all enrolled courses.
    """
    student_id: object
    courses: list[CourseReport]


def build_report_card(*, student_id) -> StudentReportCard:
    """
    Build the report card for a student.

    For each enrolled course, include:
    - all recorded numeric grades (historical)
    - numeric average (rounded to nearest integer, half-up)
    - letter average derived from the numeric average

    Notes:
    - If a student has no grades in a course yet, average is 0 and letter is derived from 0 ("F").
      This is a design choice to keep the report total and stable.
    """
    enrollments = (
        Enrollment.objects.select_related("course")
        .filter(student_id=student_id)
        .order_by("course__name")
    )

    course_reports: list[CourseReport] = []
    for e in enrollments:
        values = list(
            Grade.objects.filter(enrollment=e)
            .order_by("created_at")
            .values_list("numeric_value", flat=True)
        )

        if values:
            avg = _round_half_up(sum(values) / len(values))
        else:
            avg = 0  # design choice: no grades yet => 0

        course_reports.append(
            CourseReport(
                course_id=e.course_id,
                course_name=e.course.name,
                numeric_grades=values,
                numeric_average=avg,
                letter_average=numeric_to_letter(avg),
            )
        )

    return StudentReportCard(student_id=student_id, courses=course_reports)
