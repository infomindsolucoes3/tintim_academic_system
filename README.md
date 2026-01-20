# Academic System – Technical Challenge

This project implements the core domain of a hypothetical academic system using **Django** and **SQLite**, with emphasis on **domain modeling**, **service-layer design**, and **automated tests**.

The challenge explicitly focuses on **business logic and structure**, not on APIs or presentation layers.

---

## Domain Overview

The system models three main concepts:

- **Student**
- **Course**
- **Grade**

### Core rules

- A Student can participate in multiple Courses
- A Student cannot be enrolled in the same Course more than once
- A Student can receive multiple Grades in the same Course
- Grades are historical (append-only)
- A Grade can be provided as:
  - a numeric value (0–100), or
  - a letter concept (A+, A, A-, B+, …, F)
- Letter grades are converted to the **numeric maximum** of their range
- Numeric values are the source of truth
- Averages use **half-up rounding** (e.g. 80.5 → 81)

---

## Design Decisions

### Enrollment as an explicit entity

The relationship between Student and Course is modeled via an **Enrollment** entity to:

- enforce uniqueness
- centralize grade aggregation
- keep domain rules explicit and testable

### Service Layer

All business rules live in the **service layer**.

- Models handle structure and integrity
- Services handle domain intent and errors

### Grades

- Only numeric values are persisted
- Letter grades are derived representations
- Historical data is never mutated

---

## Project Structure (Simplified)

```
apps/
└── academics/
    ├── domain/        # models, exceptions, grade scale
    ├── services/      # business logic
    ├── tests/         # service-level tests
    └── fixtures/      # optional demo data
```

---

## Running the Project

```bash
docker compose up --build
```

---

## Running Tests

All tests validate **only domain and service behavior**.

```bash
docker compose run --rm web pytest
```

---

## Available Domain Services

### Enrollment

```python
enroll_student(student_id, course_id)
list_courses_for_student(student_id)
list_students_for_course(course_id)
```

### Grades

```python
record_grade(student_id, course_id, numeric=..., letter=...)
get_numeric_grades(student_id, course_id)
get_letter_grades(student_id, course_id)
calculate_numeric_average(student_id, course_id)
calculate_letter_average(student_id, course_id)
```

### Report Card

```python
build_report_card(student_id)
```

Returns, per course:
- recorded grades
- numeric average
- letter average

---

## Optional Demo Data (Fixtures)

An optional fixture is provided with:

- 5 students
- 1 course
- enrollments for all students
- 4 grades per student across 2025
- mixed numeric and letter-based grades (stored numerically)

Load with:

```bash
docker compose run --rm web python manage.py loaddata demo_academics.json
```

Fixtures are **not required** to run tests.

---

## Use of Artificial Intelligence

AI tools were used as **support**, mainly to:

- refresh Django configuration and patterns after several years without using the framework
- validate current best practices
- assist in drafting code under full supervision

All modeling, architectural decisions, and business rules were intentionally designed and reviewed.

---

## Notes

This project intentionally avoids APIs, serializers, and UI concerns.  
The focus is exclusively on **domain clarity**, **business rules**, **separation of responsibilities**, and **testability**, as requested.
