from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', messages, name='Messages'),
    path('chat/<id>/',messages_with,name='MessagesWith'),
    path('new/', create_message, name='NewMessage')
]
