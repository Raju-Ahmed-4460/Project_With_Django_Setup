import os
import django
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task_Management.settings')
django.setup()

from tasks.models import Employee, Project, Task, TaskDetail


def populate_db():
    fake = Faker()

    projects = []
    for _ in range(5):
        p = Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.paragraph(),
            start_data=fake.date_this_year()
        )
        projects.append(p)

    employees = []
    for _ in range(10):
        e = Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        employees.append(e)

    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(),
            description=fake.paragraph(),
            due_data=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_complete=random.choice([True, False])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)

    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            assign_to=", ".join([e.name for e in task.assigned_to.all()]),
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )