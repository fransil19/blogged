from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='Inicio'),
    path('posts/', posts, name='Posts'),
    path('users/', users, name='Users'),
    path('comments/', comments, name='Comments'),
]
