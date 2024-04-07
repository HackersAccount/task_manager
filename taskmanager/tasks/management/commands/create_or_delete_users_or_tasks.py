import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task, Epic
from django.core.exceptions import ObjectDoesNotExist

USERNAME_LENGTH = 10
PASSWORD_LENGTH = 12
DEFAULT_USER_COUNT = 30
DEFAULT_TASK_COUNT = 500
DEFAULT_EPIC_COUNT = 50
DEFAULT_TASK_STATUSES = ['UNASSIGNED', 'IN_PROGRESS', 'DONE', 'ARCHIVED']

class Command(BaseCommand):
    help = 'Create a specified number of users, tasks, and epics with random attributes'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, default=DEFAULT_USER_COUNT,
                            help='The number of users to create (default: 30)')
        parser.add_argument('-t', '--tasks', type=int, default=DEFAULT_TASK_COUNT,
                            help='The number of tasks to create (default: 500)')
        parser.add_argument('-e', '--epics', type=int, default=DEFAULT_EPIC_COUNT,
                            help='The number of epics to create (default: 50)')
        parser.add_argument('--delete', action='store_true',
                            help='Delete all existing regular users, tasks, and epics before creating new ones')

    def handle(self, *args, **kwargs):
        num_users = kwargs['users']
        num_tasks = kwargs['tasks']
        num_epics = kwargs['epics']
        should_delete = kwargs['delete']

        if should_delete:
            self.stdout.write('Deleting all existing regular users, tasks, and epics...')
            self.delete_regular_users_tasks_epics()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all existing regular users, tasks, and epics'))

        self.stdout.write(f'Creating {num_users} users...')
        for _ in range(num_users):
            username = self._generate_username()
            email = f'{username}@example.com'
            password = self._generate_password()
            User.objects.create_user(username, email, password)
        self.stdout.write(self.style.SUCCESS('Successfully created users'))

        users = User.objects.filter(is_superuser=False)  # Exclude superusers

        self.stdout.write(f'Creating {num_tasks} tasks...')
        for _ in range(num_tasks):
            try:
                creator = random.choice(users)
                owner = random.choice(users.exclude(pk=creator.pk))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR('Insufficient users for task assignment. Stopping task creation.'))
                break
            title = f'Task {_ + 1}'
            description = f'Description of Task {_ + 1}'
            status = random.choice(DEFAULT_TASK_STATUSES)
            Task.objects.create(title=title, description=description, status=status, creator=creator, owner=owner)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {min(num_tasks, _)} tasks'))

        self.stdout.write(f'Creating {num_epics} epics...')
        for _ in range(num_epics):
            try:
                creator = random.choice(users)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR('Insufficient users for epic creation. Stopping epic creation.'))
                break
            name = f'Epic {_ + 1}'
            description = f'Description of Epic {_ + 1}'
            completion_status = round(random.uniform(0.0, 100.0), 2)
            Epic.objects.create(name=name, description=description, completion_status=completion_status, creator=creator)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {min(num_epics, _)} epics'))

    def _generate_username(self, size=USERNAME_LENGTH):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def _generate_password(self, size=PASSWORD_LENGTH):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(size))

    def delete_regular_users_tasks_epics(self):
        # Delete all regular users (excluding superusers)
        User.objects.filter(is_superuser=False).delete()

        # Delete all tasks
        Task.objects.all().delete()

        # Delete all epics
        Epic.objects.all().delete()
