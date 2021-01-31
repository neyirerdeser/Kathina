from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Event(models.Model):
    name = models.TextField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.TextField(max_length=100)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(1440)])
    # scheduled_start = models.IntegerField(null=True)
    # duration_with_breaks = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def schedule(self):
        self.duration_with_breaks = (self.duration_minutes / 25) + self.duration_minutes
        self.save()
