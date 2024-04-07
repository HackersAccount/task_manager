from django.db import models
from django.contrib.auth.models import User
from typing import Optional
from datetime import datetime


# class Epic(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     creator = models.ForeignKey(
#         User,
#         related_name='created_epics',   
#         on_delete=models.CASCADE
#     )


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

    title: str = models.CharField(max_length=200, verbose_name="Title")
    description: str = models.TextField(blank=True, null=False, default="", verbose_name="Description")
    status: str = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="UNASSIGNED",
        db_comment="Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED.",
        verbose_name="Status"
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at: datetime = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    creator: User = models.ForeignKey(
        User, 
        related_name="created_tasks", 
        on_delete=models.CASCADE,
        verbose_name="Creator"
    )
    owner: Optional[User] = models.ForeignKey(
        User,
        related_name="owned_tasks",
        on_delete=models.SET_NULL,
        null=True,
        db_comment="Foreign Key to the User who currently owns the task.",
        verbose_name="Owner"
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table_comment = "Holds information about tasks"

    def __str__(self) -> str:
        return self.title



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Other fields…


# class Sprint(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     creator = models.ForeignKey(
#         User,
#         related_name='created_sprints', 
#         on_delete=models.CASCADE
#     )
#     tasks = models.ManyToManyField(
#         'Task',
#         related_name='sprints', 
#         blank=True
#     )

#     class Meta:
#         constraints = [
#             models.CheckConstraint(check=models.Q(end_date__gt=models.
#             F('start_date')), name='end_date_after_start_date'),
#         ]
