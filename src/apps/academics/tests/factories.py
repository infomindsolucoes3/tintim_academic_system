import factory

from apps.academics.domain.models import Student, Course, Enrollment, Grade


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    name = factory.Sequence(lambda n: f"Student {n}")


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.Sequence(lambda n: f"Course {n}")


class EnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment

    student = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade

    enrollment = factory.SubFactory(EnrollmentFactory)
    numeric_value = 100
