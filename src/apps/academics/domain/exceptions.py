from apps.academics.domain.types import UUID

class DomainError(Exception):
    """
    Base class for all domain-level errors.

    Domain errors represent violations of business rules and
    must never be silently ignored.
    """
    pass


class DuplicateEnrollmentError(DomainError):
    """
    Raised when attempting to enroll a student in a course
    they already participate in.
    """
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"Student {student_id} is already enrolled in course {course_id}."
        )


class StudentNotEnrolledError(DomainError):
    """
    Raised when attempting to perform an action that requires
    a student to be enrolled in a course, but no enrollment exists.
    """
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"Student {student_id} is not enrolled in course {course_id}."
        )


class InvalidGradeInputError(DomainError):
    """
    Raised when grade input is invalid.

    Examples:
    - both numeric and letter grades are provided
    - neither numeric nor letter grade is provided
    - grade value is out of allowed range
    """
    def __init__(self, message: str):
        super().__init__(message)


class InvalidLetterGradeError(DomainError):
    """
    Raised when a letter grade does not match the supported scale.
    """
    def __init__(self, letter: str):
        super().__init__(f"Invalid letter grade: '{letter}'.")


class NoGradesRecordedError(DomainError):
    """
    Raised when an aggregation (e.g., average) is requested but no grades exist.
    """
    def __init__(self, student_id: UUID, course_id: UUID):
        super().__init__(
            f"No grades recorded for student {student_id} in course {course_id}."
        )


class InvalidStudentNameError(DomainError):
    def __init__(self, name: str):
        super().__init__(f"Invalid student name: {name!r}.")


class InvalidCourseNameError(DomainError):
    def __init__(self, name: str):
        super().__init__(f"Invalid course name: {name!r}.")
