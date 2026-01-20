import pytest

from apps.academics.domain.exceptions import InvalidStudentNameError, InvalidCourseNameError
from apps.academics.services.registration import create_student, create_course


@pytest.mark.django_db
def test_create_student_success_strips_name():
    s = create_student(name="  Alice  ")
    assert s.name == "Alice"


@pytest.mark.django_db
def test_create_student_rejects_blank_name():
    with pytest.raises(InvalidStudentNameError):
        create_student(name="   ")


@pytest.mark.django_db
def test_create_course_success_strips_name():
    c = create_course(name="  Physics  ")
    assert c.name == "Physics"


@pytest.mark.django_db
def test_create_course_rejects_blank_name():
    with pytest.raises(InvalidCourseNameError):
        create_course(name="")
