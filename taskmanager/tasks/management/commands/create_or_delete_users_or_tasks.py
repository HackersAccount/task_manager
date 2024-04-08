import random
import string

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Task, Epic, Sprint
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from typing import Any, Dict, List

# Constants for default values
USERNAME_LENGTH: int = 10
PASSWORD_LENGTH: int = 12
DEFAULT_USER_COUNT: int = 30
DEFAULT_TASK_COUNT: int = 500
DEFAULT_EPIC_COUNT: int = 50
DEFAULT_SPRINT_COUNT: int = 10
DEFAULT_TASK_STATUSES: List[str] = ['UNASSIGNED', 'IN_PROGRESS', 'DONE', 'ARCHIVED']

class Command(BaseCommand):
    help: str = 'Create a specified number of users, tasks, epics, and sprints with random attributes'

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument('-u', '--users', type=int, default=DEFAULT_USER_COUNT,
                            help='The number of users to create (default: 30)')
        parser.add_argument('-t', '--tasks', type=int, default=DEFAULT_TASK_COUNT,
                            help='The number of tasks to create (default: 500)')
        parser.add_argument('-e', '--epics', type=int, default=DEFAULT_EPIC_COUNT,
                            help='The number of epics to create (default: 50)')
        parser.add_argument('-s', '--sprints', type=int, default=DEFAULT_SPRINT_COUNT,
                            help='The number of sprints to create (default: 10)')
        parser.add_argument('--delete', action='store_true',
                            help='Delete all existing regular users, tasks, epics, and sprints before creating new ones')

    def handle(self, *args: Any, **kwargs: Any) -> None:
        num_users: int = kwargs['users']
        num_tasks: int = kwargs['tasks']
        num_epics: int = kwargs['epics']
        num_sprints: int = kwargs['sprints']
        should_delete: bool = kwargs['delete']

        if should_delete:
            self.stdout.write('Deleting all existing regular users, tasks, epics, and sprints...')
            self.delete_regular_users_tasks_epics_sprints()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all existing regular users, tasks, epics, and sprints'))

        self.create_users(num_users)
        self.create_tasks(num_tasks)
        self.create_epics(num_epics)
        self.create_sprints(num_sprints)

    def create_users(self, num_users: int) -> None:
        """
        Create a specified number of users with random attributes.

        Args:
            num_users (int): The number of users to create.
        """
        self.stdout.write(f'Creating {num_users} users...')
        for _ in range(num_users):
            username: str = self._generate_username()
            email: str = f'{username}@example.com'
            password: str = self._generate_password()
            User.objects.create_user(username, email, password)
        self.stdout.write(self.style.SUCCESS('Successfully created users'))

    def create_tasks(self, num_tasks: int) -> None:
        """
        Create a specified number of tasks with random attributes.

        Args:
            num_tasks (int): The number of tasks to create.
        """
        users: List[User] = User.objects.filter(is_superuser=False)
        self.stdout.write(f'Creating {num_tasks} tasks...')
        for _ in range(num_tasks):
            try:
                creator: User = random.choice(users)
                owner: User = random.choice(users.exclude(pk=creator.pk))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR('Insufficient users for task assignment. Stopping task creation.'))
                break
            title: str = f'Task {_ + 1}'
            description: str = f'Description of Task {_ + 1}'
            status: str = random.choice(DEFAULT_TASK_STATUSES)
            Task.objects.create(title=title, description=description, status=status, creator=creator, owner=owner)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {min(num_tasks, 0)} tasks'))

    def create_epics(self, num_epics: int) -> None:
        """
        Create a specified number of epics with random attributes.

        Args:
            num_epics (int): The number of epics to create.
        """
        users: List[User] = User.objects.filter(is_superuser=False)
        self.stdout.write(f'Creating {num_epics} epics...')
        for _ in range(num_epics):
            try:
                creator: User = random.choice(users)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR('Insufficient users for epic creation. Stopping epic creation.'))
                break
            name: str = f'Epic {_ + 1}'
            description: str = f'Description of Epic {_ + 1}'
            completion_status: float = round(random.uniform(0.0, 100.0), 2)
            Epic.objects.create(name=name, description=description, completion_status=completion_status, creator=creator)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {min(num_epics, 0)} epics'))

    def create_sprints(self, num_sprints: int) -> None:
        """
        Create a specified number of sprints with random attributes.

        Args:
            num_sprints (int): The number of sprints to create.
        """
        users: List[User] = User.objects.filter(is_superuser=False)
        self.stdout.write(f'Creating {num_sprints} sprints...')
        for _ in range(num_sprints):
            try:
                creator: User = random.choice(users)
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR('Insufficient users for sprint creation. Stopping sprint creation.'))
                break
            name: str = f'Sprint {_ + 1}'
            description: str = f'Description of Sprint {_ + 1}'
            start_date: timezone.datetime = timezone.now().date()  # Adjust as needed
            end_date: timezone.datetime = start_date + timezone.timedelta(days=random.randint(7, 14))  # Adjust as needed
            Sprint.objects.create(name=name, description=description, start_date=start_date, end_date=end_date, creator=creator)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {min(num_sprints, 0)} sprints'))

    def _generate_username(self, size: int = USERNAME_LENGTH) -> str:
        """
        Generate a random username.

        Args:
            size (int): The length of the username.

        Returns:
            str: A randomly generated username.
        """
        chars: str = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def _generate_password(self, size: int = PASSWORD_LENGTH) -> str:
        """
        Generate a random password.

        Args:
            size (int): The length of the password.

        Returns:
            str: A randomly generated password.
        """
        chars: str = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(size))

    def delete_regular_users_tasks_epics_sprints(self) -> None:
        """
        Delete all regular users, tasks, epics, and sprints.
        """
        # Delete all regular users (excluding superusers)
        User.objects.filter(is_superuser=False).delete()

        # Delete all tasks
        Task.objects.all().delete()

        # Delete all epics
        Epic.objects.all().delete()

        # Delete all sprints
        Sprint.objects.all().delete()
