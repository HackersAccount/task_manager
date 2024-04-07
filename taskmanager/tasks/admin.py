from django.contrib import admin
from tasks.models import Task  

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

# Register the TaskAdmin with the Task model
admin.site.register(Task, TaskAdmin)

# Customize admin header and title
admin.site.site_header = "Task Manager Admin"
admin.site.site_title = "Task Manager"
admin.site.index_title = "Welcome to the Task Manager Admin Dashboard"
