from django.utils import timezone, timesince
from django.conf import settings
from django.db.models import Q
from tasks.models import Task

settings.configure()

Task.objects.exclude(   )