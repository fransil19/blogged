from enum import unique
from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class formPost(forms.Form):
    title = forms.CharField(max_length=70)
    subtitle = forms.CharField(max_length=150)
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":150}))
    #author = forms.ModelChoiceField(queryset=User.objects.all())
    image = forms.ImageField()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", widget= forms.PasswordInput)
    password2 = forms.CharField(label="Repeat the password", widget= forms.PasswordInput)

    name = forms.CharField(max_length=40)
    surname = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ["name","surname","username","email","password1","password2"]

        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm the password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email","username","password1","password2"]

        help_texts = {k:"" for k in fields}


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=70)
    subtitle = forms.CharField(max_length=150)
    autor = forms.ModelChoiceField(queryset=User.objects.all())
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":150}))
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ["title","subtitle","autor","content","image"]

class AvatarForm(forms.Form):
    image = forms.ImageField()