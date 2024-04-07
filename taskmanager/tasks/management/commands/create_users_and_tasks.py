from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task
import random

class Command(BaseCommand):
    help = 'Create 30 unique users and 500 tasks'

    def handle(self, *args, **kwargs):
        # Create 30 unique users
        for i in range(1, 31):
            username = f'user_{i}'
            email = f'user_{i}@example.com'
            password = 'password'  # You may want to generate a random password
            User.objects.create_user(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS('Successfully created 30 users'))

        # Create 500 tasks
        users = User.objects.all()
        statuses = ['UNASSIGNED', 'IN_PROGRESS', 'DONE', 'ARCHIVED']

        for _ in range(500):
            title = f'Task {_ + 1}'
            description = f'Description of Task {_ + 1}'
            status = random.choice(statuses)
            creator = random.choice(users)
            owner = random.choice(users)
            Task.objects.create(title=title, description=description, status=status, creator=creator, owner=owner)

        self.stdout.write(self.style.SUCCESS('Successfully created 500 tasks'))
