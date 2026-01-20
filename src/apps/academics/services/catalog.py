from __future__ import annotations

from dataclasses import dataclass

from apps.academics.domain.models import Student, Course


@dataclass(frozen=True)
class StudentSummary:
    id: object
    name: str


@dataclass(frozen=True)
class CourseSummary:
    id: object
    name: str


def list_students() -> list[StudentSummary]:
    """
    List students (id + name) to make manual exploration easier.
    """
    return [
        StudentSummary(id=s.id, name=s.name)
        for s in Student.objects.order_by("name")
    ]


def list_courses() -> list[CourseSummary]:
    """
    List courses (id + name) to make manual exploration easier.
    """
    return [
        CourseSummary(id=c.id, name=c.name)
        for c in Course.objects.order_by("name")
    ]
