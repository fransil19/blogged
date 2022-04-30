from datetime import date
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.today)
    user_from = models.ForeignKey(User, related_name="user_from", on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="user_to", on_delete=models.CASCADE)

