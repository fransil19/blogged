from enum import unique
from django import forms

class formPost(forms.Form):
    title = forms.CharField(max_length=70)
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":150}))
    #user = forms.ModelChoiceField(queryset=User.objects.all())
    
class formUser(forms.Form):
    name = forms.CharField(max_length=40)
    surname = forms.CharField(max_length=40)
    email = forms.EmailField()

class formComment(forms.Form):
    text = forms.CharField(max_length=200) 