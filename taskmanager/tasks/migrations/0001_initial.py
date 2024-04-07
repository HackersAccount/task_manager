# Generated by Django 4.2.2 on 2024-04-07 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('status', models.CharField(choices=[('UNASSIGNED', 'Unassigned'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Completed'), ('ARCHIVED', 'Archived')], db_comment='Can be UNASSIGNED, IN_PROGRESS, DONE, or ARCHIVED.', default='UNASSIGNED', max_length=20, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('owner', models.ForeignKey(db_comment='Foreign Key to the User who currently owns the task.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'db_table_comment': 'Holds information about tasks',
            },
        ),
    ]