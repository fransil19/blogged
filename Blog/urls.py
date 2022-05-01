from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index, name='Index'),
    path('about/', about, name='About'),   
    
    path('pages/', PostList.as_view(), name="Posts"),
    path('pages/detail/<pk>', PostDetail.as_view(), name="PostDetail"),
    path('pages/new/', login_required(PostCreate.as_view()), name="PostCreate"),
    path('pages/edit/<pk>', PostUpdate.as_view(), name="PostEdit"),
    path('pages/delete/<pk>', PostDelete.as_view(), name="PostDelete"),

    path('accounts/login/', login_request, name="Login"),
    path('accounts/signup/', register, name='Register'),
    path('accounts/logout/', LogoutView.as_view(template_name='Blog/logout.html'), name='Logout'),
    path('accounts/profile/', editProfile, name='Profile'),
    path('accounts/addAvatar/', addAvatar, name='AddAvatar'),
    path('accounts/deleteAvatar/', delete_avatar, name='DeleteAvatar'),
]
