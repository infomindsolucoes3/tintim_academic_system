
# Create your models here.
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Abstract base model that uses UUID as primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Student(UUIDModel, TimeStampedModel):
    """
    Represents a student in the academic system.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Course(UUIDModel, TimeStampedModel):
    """
    Represents a course that students can participate in.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Enrollment(UUIDModel, TimeStampedModel):
    """
    Represents the participation of a student in a course.

    A student can participate in many courses,
    but only once per course.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment",
            )
        ]

    def __str__(self) -> str:
        return f"{self.student} -> {self.course}"


class Grade(UUIDModel, TimeStampedModel):
    """
    Represents a grade assigned to a student in a course.

    Grades are historical records: multiple grades may exist
    for the same enrollment.

    The numeric_value field is the primary source of truth.
    Letter grades are derived representations and should not
    be persisted as source data.
    """
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="grades",
    )

    numeric_value = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    def __str__(self) -> str:
        return f"{self.enrollment} -> {self.numeric_value}"
