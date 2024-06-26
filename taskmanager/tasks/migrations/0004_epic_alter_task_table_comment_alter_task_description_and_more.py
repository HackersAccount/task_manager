# Generated by Django 4.2.2 on 2024-04-07 17:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_auto_20240407_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('completion_status', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Completion Status (percentage)')),
            ],
            options={
                'verbose_name': 'Epic',
                'verbose_name_plural': 'Epics',
            },
        ),
        migrations.AlterModelTableComment(
            name='task',
            table_comment=None,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('UNASSIGNED', 'Unassigned'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Completed'), ('ARCHIVED', 'Archived')], default='UNASSIGNED', max_length=20, verbose_name='Status'),
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.CheckConstraint(check=models.Q(('status', 'UNASSIGNED'), ('status', 'IN_PROGRESS'), ('status', 'DONE'), ('status', 'ARCHIVED'), _connector='OR'), name='status_check'),
        ),
        migrations.AddField(
            model_name='epic',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_epics', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='epic',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='epics', to='tasks.task'),
        ),
    ]
