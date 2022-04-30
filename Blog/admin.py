from django.contrib import admin

from messagges.models import Message
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Avatar)
admin.site.register(Message)
