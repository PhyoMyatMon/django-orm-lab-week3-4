
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "training_system.settings")
django.setup()

from django.db import connection, reset_queries
from django.db.models import Q, F
from core.models import Employee, Course

# TASK 4.1: Q OBJECTS

query_or = Employee.objects.filter(
    Q(department__code="IT") | Q(salary__gt=70000)
)
print("OR Query Results:", list(query_or))

query_not = Employee.objects.filter(
    Q(first_name__icontains="John") & ~Q(department__code="HR")
)
print("AND NOT Query Results:", list(query_not))


# TASK 4.2: F EXPRESSIONS
# Display updated salaries (the 10% update was already performed)
for emp in Employee.objects.filter(department__code="IT"):
    print(f"{emp.first_name} New Salary: {emp.salary}")


# TASK 4.3: UNOPTIMIZED QUERY

reset_queries()
employees = Employee.objects.all()

for emp in employees:
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")

print("Unoptimized Queries:", len(connection.queries))


# SELECT_RELATED()

reset_queries()
employees = Employee.objects.select_related("department").all()

for emp in employees:
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")

print("select_related Queries:", len(connection.queries))


# PREFETCH_RELATED()

reset_queries()
courses = Course.objects.prefetch_related("attendees").all()

for course in courses:
    names = [emp.first_name for emp in course.attendees.all()]
    print(f"Course: {course.code}, Attendees: {', '.join(names)}")

print("prefetch_related Queries:", len(connection.queries))
