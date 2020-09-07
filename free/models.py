from django.db import models
from django.contrib.auth.models import User
import datetime

class subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    end_date = models.DateTimeField()

class subscriptionFix(models.Model):
    user = models.TextField(unique=True) # user = models.CharField(max_length=100, unique=True) on server due to mysql limits
    end_date = models.DateTimeField(blank=True, null=True)

class transaction(models.Model):
    user = models.TextField(default='santa')
    tax = models.FloatField(blank=True)
    address = models.TextField()
    zip = models.IntegerField()
    state = models.TextField()
    city = models.TextField()
    commit = models.BooleanField()
    date = models.DateTimeField(default=datetime.datetime.now())
