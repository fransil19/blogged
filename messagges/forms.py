from enum import unique
from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":150}))

class NewMessageForm(forms.Form):
    user_to = forms.ModelChoiceField(queryset=User.objects.all())
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":150}))

