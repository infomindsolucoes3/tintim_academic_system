import pytest

from apps.academics.services.queries import list_courses_for_student, list_students_for_course
from apps.academics.tests.factories import CourseFactory, EnrollmentFactory, StudentFactory


@pytest.mark.django_db
def test_list_courses_for_student_returns_enrolled_courses():
    student = StudentFactory()
    course_a = CourseFactory(name="Algebra")
    course_b = CourseFactory(name="Biology")

    EnrollmentFactory(student=student, course=course_b)
    EnrollmentFactory(student=student, course=course_a)

    courses = list_courses_for_student(student_id=student.id)

    assert [c.name for c in courses] == ["Algebra", "Biology"]


@pytest.mark.django_db
def test_list_students_for_course_returns_enrolled_students():
    course = CourseFactory(name="Physics")
    s1 = StudentFactory(name="Ana")
    s2 = StudentFactory(name="Bruno")

    EnrollmentFactory(student=s2, course=course)
    EnrollmentFactory(student=s1, course=course)

    students = list_students_for_course(course_id=course.id)

    assert [s.name for s in students] == ["Ana", "Bruno"]
