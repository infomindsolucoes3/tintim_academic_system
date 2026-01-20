from django.db import IntegrityError, transaction

from apps.academics.domain.exceptions import DuplicateEnrollmentError
from apps.academics.domain.models import Enrollment
from apps.academics.domain.types import UUID



@transaction.atomic
def enroll_student(*, student_id: UUID, course_id: UUID) -> Enrollment:
    """
    Enroll a student into a course.

    Rules:
    - A student cannot be enrolled in the same course more than once.
    - Duplicate enrollment attempts raise an explicit domain error.
    """
    if Enrollment.objects.filter(
        student_id=student_id,
        course_id=course_id,
    ).exists():
        raise DuplicateEnrollmentError(student_id=student_id, course_id=course_id)

    return Enrollment.objects.create(
        student_id=student_id,
        course_id=course_id,
    )