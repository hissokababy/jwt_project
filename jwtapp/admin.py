from django.contrib import admin

from jwtapp.models import Session, User

# Register your models here.

admin.site.register(Session)
admin.site.register(User)
