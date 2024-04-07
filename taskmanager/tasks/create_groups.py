from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    # Get the ContentType object for the Task model
    task_content_type = ContentType.objects.get(app_label='tasks', model='task')

    # Create "Creator" group with "add_task" permission
    creator_group, _ = Group.objects.get_or_create(name='Creator')
    add_task_permission, _ = Permission.objects.get_or_create(codename='add_task', content_type=task_content_type)
    creator_group.permissions.add(add_task_permission)

    # Create "Editor" group with "change_task" permission
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    change_task_permission, _ = Permission.objects.get_or_create(codename='change_task', content_type=task_content_type)
    editor_group.permissions.add(change_task_permission)

    # Create "Admin" group with all permissions
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    all_permissions = Permission.objects.filter(content_type=task_content_type)
    admin_group.permissions.set(all_permissions)
