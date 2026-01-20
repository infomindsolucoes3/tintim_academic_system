from __future__ import annotations

from apps.academics.domain.exceptions import InvalidStudentNameError, InvalidCourseNameError
from apps.academics.domain.models import Student, Course


def create_student(*, name: str) -> Student:
    """
    Create a Student with the minimal required attributes.
    """
    normalized = (name or "").strip()
    if not normalized:
        raise InvalidStudentNameError(name=name)
    return Student.objects.create(name=normalized)


def create_course(*, name: str) -> Course:
    """
    Create a Course with the minimal required attributes.
    """
    normalized = (name or "").strip()
    if not normalized:
        raise InvalidCourseNameError(name=name)
    return Course.objects.create(name=normalized)
