from django.db import IntegrityError, transaction

from apps.academics.domain.exceptions import DuplicateEnrollmentError
from apps.academics.domain.models import Enrollment


@transaction.atomic
def enroll_student(*, student_id, course_id) -> Enrollment:
    """
    Enroll a student into a course.

    Rules:
    - A student cannot be enrolled in the same course more than once.
    - Duplicate enrollment attempts raise an explicit domain error.
    """
    try:
        return Enrollment.objects.create(student_id=student_id, course_id=course_id)
    except IntegrityError:
        # UniqueConstraint(student, course) is enforced at DB level.
        raise DuplicateEnrollmentError(student_id=student_id, course_id=course_id)
