# Generated by Django 4.2.2 on 2024-04-07 17:03

from django.db import migrations
# Import the function to create groups
from tasks.create_groups import create_groups

# Define the migration operation
create_groups_operation = migrations.RunPython(create_groups)

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20240407_1424'),
    ]

    operations = [
        create_groups_operation
    ]
