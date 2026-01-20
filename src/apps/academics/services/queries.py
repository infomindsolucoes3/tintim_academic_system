from __future__ import annotations

from apps.academics.domain.models import Course, Enrollment, Student


def list_courses_for_student(*, student_id) -> list[Course]:
    """
    Return all courses a student is enrolled in.
    """
    return list(
        Course.objects.filter(enrollments__student_id=student_id)
        .order_by("name")
        .distinct()
    )


def list_students_for_course(*, course_id) -> list[Student]:
    """
    Return all students enrolled in a given course.
    """
    return list(
        Student.objects.filter(enrollments__course_id=course_id)
        .order_by("name")
        .distinct()
    )
