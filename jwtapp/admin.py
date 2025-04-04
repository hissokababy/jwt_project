from django.contrib import admin

from jwtapp.models import RefreshToken, Session

# Register your models here.

admin.site.register(Session)
admin.site.register(RefreshToken)