from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Epic(models.Model):
    """
    Represents a project epic.

    An epic is a large body of work that can be broken down into smaller tasks.
    """

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    completion_status = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name=_("Completion Status (percentage)"))
    creator = models.ForeignKey(User, related_name='created_epics', on_delete=models.CASCADE, verbose_name=_("Creator"))
    tasks = models.ManyToManyField("Task", related_name="epics", blank=True)

    class Meta:
        verbose_name = _("Epic")
        verbose_name_plural = _("Epics")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure updated_at field is always updated.
        """
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def tasks_count(self) -> int:
        """
        Calculates and returns the total number of tasks associated with this epic.

        Returns:
            int: Total number of tasks.
        """
        return self.tasks.count()

    @property
    def completed_tasks_count(self) -> int:
        """
        Calculates and returns the number of completed tasks associated with this epic.

        Returns:
            int: Number of completed tasks.
        """
        return self.tasks.filter(status='DONE').count()

    @property
    def completion_percentage(self) -> float:
        """
        Calculates and returns the completion percentage of this epic based on its tasks.

        Returns:
            float: Completion percentage.
        """
        if self.tasks_count == 0:
            return 0.0
        return (self.completed_tasks_count / self.tasks_count) * 100


class Task(models.Model):
    """
    Represents a task in the system.
    """
    STATUS_CHOICES = [
        ("UNASSIGNED", "Unassigned"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Completed"),
        ("ARCHIVED", "Archived"),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="UNASSIGNED", 
        verbose_name=_("Status")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    creator = models.ForeignKey(
        User, 
        related_name="created_tasks", 
        on_delete=models.CASCADE, 
        verbose_name=_("Creator")
    )
    owner = models.ForeignKey(
        User, 
        related_name="owned_tasks", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("Owner")
    )


    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        constraints = [
            models.CheckConstraint(
                check=models.Q(status="UNASSIGNED")
                | models.Q(status="IN_PROGRESS")
                | models.Q(status="DONE")
                | models.Q(status="ARCHIVED"),
                name="status_check",
            ),
        ]

    def __str__(self):
        return self.title
    

class Sprint(models.Model):
    """
    Represents a sprint in the project management system.
    """

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Updated At")
    )
    creator = models.ForeignKey(
        User, related_name='created_sprints', 
        on_delete=models.CASCADE, 
        verbose_name=_("Creator")
    )
    epic = models.ForeignKey(
        Epic, 
        related_name="sprints",
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=_("Sprint")
    )
    tasks = models.ManyToManyField(
        "Task", 
        related_name="sprints", 
        blank=True
    )
    class Meta:
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='end_date_after_start_date'
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def duration(self):
        """
        Calculates the duration of the sprint in days.

        Returns:
            int: Duration of the sprint in days.
        """
        return (self.end_date - self.start_date).days

    @property
    def total_tasks(self):
        """
        Calculates the total number of tasks associated with the sprint.

        Returns:
            int: Total number of tasks associated with the sprint.
        """
        return self.tasks.count()

    @property
    def completed_tasks(self):
        """
        Calculates the number of completed tasks associated with the sprint.

        Returns:
            int: Number of completed tasks associated with the sprint.
        """
        return self.tasks.filter(status='DONE').count()

    @property
    def completion_percentage(self):
        """
        Calculates the completion percentage of the sprint based on completed tasks.

        Returns:
            float: Completion percentage of the sprint.
        """
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100
