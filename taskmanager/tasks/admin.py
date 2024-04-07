from django.contrib import admin
from tasks.models import Epic, Task, Sprint
from django.http import HttpRequest


class TaskAdmin(admin.ModelAdmin):
    # Customize the display of tasks in the admin list
    list_display = ("title", "description", "status", "owner", "created_at", "updated_at")
    # Add filter options for task status
    list_filter = ("status",)
    # Enable search functionality for task title, description, and owner
    search_fields = ("title", "description", "owner__username")

    def mark_archived(self, request, queryset):
        """
        Custom admin action to mark selected tasks as archived.

        Parameters:
            - self: The instance of the TaskAdmin class.
            - request: The HTTP request object.
            - queryset: A queryset containing the selected tasks.

        Returns:
            None
        """
        # Update the status of selected tasks to "ARCHIVED"
        queryset.update(status="ARCHIVED")

    # Set a short description for the custom action in the admin interface
    mark_archived.short_description = 'Mark selected tasks as archived'

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to change tasks.

        Args:
            request: The HTTP request object.
            obj: The object being changed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.change_task')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check if the user has permission to add tasks.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.add_task')

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to delete tasks.

        Args:
            request: The HTTP request object.
            obj: The object being deleted.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.delete_task')


class EpicAdmin(admin.ModelAdmin):
    # Customize the display of epics in the admin list
    list_display = ("name", "description", "creator", "completion_status", "created_at", "updated_at")
    # Add filter options for epic creator and completion status
    list_filter = ("creator", "completion_status")
    # Enable search functionality for epic name and creator
    search_fields = ("name", "creator__username")

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to change epics.

        Args:
            request: The HTTP request object.
            obj: The object being changed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.change_epic')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check if the user has permission to add epics.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.add_epic')

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to delete epics.

        Args:
            request: The HTTP request object.
            obj: The object being deleted.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.delete_epic')


class SprintAdmin(admin.ModelAdmin):
    # Customize the display of sprints in the admin list
    list_display = ("name", "description", "start_date", "end_date", "creator", "created_at", "updated_at")
    # Add filter options for sprint creator and start date
    list_filter = ("creator", "start_date")
    # Enable search functionality for sprint name and creator
    search_fields = ("name", "creator__username")

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to change sprints.

        Args:
            request: The HTTP request object.
            obj: The object being changed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.change_sprint')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check if the user has permission to add sprints.

        Args:
            request: The HTTP request object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.add_sprint')

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """
        Check if the user has permission to delete sprints.

        Args:
            request: The HTTP request object.
            obj: The object being deleted.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm('tasks.delete_sprint')


# Register the models with their respective admins
admin.site.register(Epic, EpicAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)

# Customize admin header and title
admin.site.site_header = "Task Manager Admin"
admin.site.site_title = "Task Manager"
admin.site.index_title = "Welcome to the Task Manager Admin Dashboard"
