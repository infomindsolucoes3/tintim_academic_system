import pytest

from apps.academics.domain.exceptions import DuplicateEnrollmentError
from apps.academics.domain.models import Enrollment
from apps.academics.services.enrollments import enroll_student
from apps.academics.tests.factories import StudentFactory, CourseFactory, EnrollmentFactory


@pytest.mark.django_db
def test_enroll_student_creates_enrollment():
    student = StudentFactory()
    course = CourseFactory()

    enrollment = enroll_student(student_id=student.id, course_id=course.id)

    assert enrollment.student_id == student.id
    assert enrollment.course_id == course.id
    assert Enrollment.objects.filter(student=student, course=course).exists()


@pytest.mark.django_db
def test_enroll_student_raises_on_duplicate_enrollment():
    enrollment = EnrollmentFactory()

    with pytest.raises(DuplicateEnrollmentError):
        enroll_student(student_id=enrollment.student_id, course_id=enrollment.course_id)
