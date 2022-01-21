from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

BUS_TYPES = (
    ('EXP', 'express'),
    ('REG', 'regular')
)

class Bus(models.Model):
    name = models.CharField(max_length=20, default="bus_to_belize1")
    plate_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=35)
    date_created = models.DateTimeField(default=timezone.now)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL , null=True, related_name="busDriver")
    conductor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="conductor")

    def __str__(self):
        return self.name
    

