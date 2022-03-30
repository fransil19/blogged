import email
from pyexpat import model
from tkinter import CASCADE, Widget
from xmlrpc.client import DateTime
from django.db import models
import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(unique=True)
    date = models.DateTimeField(default=datetime.datetime.today)

class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateField(default=datetime.datetime.today)
