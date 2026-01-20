import pytest

from apps.academics.services.report_cards import build_report_card
from apps.academics.services.grades import record_grade
from apps.academics.tests.factories import CourseFactory, EnrollmentFactory, StudentFactory


@pytest.mark.django_db
def test_build_report_card_empty_when_no_enrollments():
    student = StudentFactory()

    report = build_report_card(student_id=student.id)

    assert report.student_id == student.id
    assert report.courses == []


@pytest.mark.django_db
def test_build_report_card_includes_courses_and_aggregates_grades():
    student = StudentFactory(name="Andre")
    course_math = CourseFactory(name="Math")
    course_history = CourseFactory(name="History")

    e_math = EnrollmentFactory(student=student, course=course_math)
    EnrollmentFactory(student=student, course=course_history)

    # Math: 80, 81 => avg 80.5 => 81 => B-
    record_grade(student_id=student.id, course_id=course_math.id, numeric=80)
    record_grade(student_id=student.id, course_id=course_math.id, numeric=81)

    report = build_report_card(student_id=student.id)

    # Sorted by course name: History, Math
    assert [c.course_name for c in report.courses] == ["History", "Math"]

    history = report.courses[0]
    assert history.numeric_grades == []
    assert history.numeric_average == 0
    assert history.letter_average == "F"

    math = report.courses[1]
    assert math.course_id == e_math.course_id
    assert math.numeric_grades == [80, 81]
    assert math.numeric_average == 81
    assert math.letter_average == "B-"


@pytest.mark.django_db
def test_build_report_card_records_letter_input_as_numeric_max():
    student = StudentFactory()
    course = CourseFactory(name="Chemistry")
    EnrollmentFactory(student=student, course=course)

    # "A" => numeric max 96
    record_grade(student_id=student.id, course_id=course.id, letter="A")

    report = build_report_card(student_id=student.id)
    assert len(report.courses) == 1

    c = report.courses[0]
    assert c.numeric_grades == [96]
    assert c.numeric_average == 96
    assert c.letter_average == "A"
