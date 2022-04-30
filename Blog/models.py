from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=70)
    subtitle = models.CharField(max_length=150)
    content = models.TextField(unique=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'images', null=True, blank = True)

    def __str__(self):
        return f"Title: {self.title} - Text: - Date {self.date}"

""" class UserProfile(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Name: {self.name} - Surname {self.surname} - Email {self.email}"

class Comment(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return f"Text: {self.text[:30]}... - Date {self.date}"
 """
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'avatars', null=True, blank = True)
