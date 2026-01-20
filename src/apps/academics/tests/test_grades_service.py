import pytest

from apps.academics.domain.exceptions import (
    InvalidGradeInputError,
    InvalidLetterGradeError,
    NoGradesRecordedError,
    StudentNotEnrolledError,
)
from apps.academics.services.grades import (
    calculate_letter_average,
    calculate_numeric_average,
    get_letter_grades,
    get_numeric_grades,
    record_grade,
)
from apps.academics.tests.factories import StudentFactory, CourseFactory, EnrollmentFactory


@pytest.mark.django_db
def test_record_grade_requires_enrollment():
    student = StudentFactory()
    course = CourseFactory()

    with pytest.raises(StudentNotEnrolledError):
        record_grade(student_id=student.id, course_id=course.id, numeric=80)


@pytest.mark.django_db
def test_record_grade_accepts_numeric():
    enrollment = EnrollmentFactory()

    g = record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, numeric=80)

    assert g.enrollment_id == enrollment.id
    assert g.numeric_value == 80


@pytest.mark.django_db
def test_record_grade_accepts_letter_and_stores_numeric_max():
    enrollment = EnrollmentFactory()

    g = record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, letter="A")

    assert g.numeric_value == 96  # max of A range


@pytest.mark.django_db
def test_record_grade_rejects_both_numeric_and_letter():
    enrollment = EnrollmentFactory()

    with pytest.raises(InvalidGradeInputError):
        record_grade(
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            numeric=80,
            letter="B",
        )


@pytest.mark.django_db
def test_record_grade_rejects_neither_numeric_nor_letter():
    enrollment = EnrollmentFactory()

    with pytest.raises(InvalidGradeInputError):
        record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id)


@pytest.mark.django_db
def test_record_grade_rejects_out_of_range_numeric():
    enrollment = EnrollmentFactory()

    with pytest.raises(InvalidGradeInputError):
        record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, numeric=101)


@pytest.mark.django_db
def test_record_grade_rejects_invalid_letter():
    enrollment = EnrollmentFactory()

    with pytest.raises(InvalidLetterGradeError):
        record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, letter="Z")


@pytest.mark.django_db
def test_get_grades_and_averages():
    enrollment = EnrollmentFactory()

    record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, numeric=80)
    record_grade(student_id=enrollment.student_id, course_id=enrollment.course_id, numeric=81)

    assert get_numeric_grades(student_id=enrollment.student_id, course_id=enrollment.course_id) == [80, 81]
    assert get_letter_grades(student_id=enrollment.student_id, course_id=enrollment.course_id) == ["B-", "B-"]

    # average = 80.5 -> must round to nearest integer (half up) => 81
    assert calculate_numeric_average(student_id=enrollment.student_id, course_id=enrollment.course_id) == 81
    assert calculate_letter_average(student_id=enrollment.student_id, course_id=enrollment.course_id) == "B-"


@pytest.mark.django_db
def test_average_requires_at_least_one_grade():
    enrollment = EnrollmentFactory()

    with pytest.raises(NoGradesRecordedError):
        calculate_numeric_average(student_id=enrollment.student_id, course_id=enrollment.course_id)
