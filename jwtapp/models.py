from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
week = datetime.timedelta(days=7)

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name='Пользователь')
    is_active = models.BooleanField(default=False, verbose_name='Активная сессия')

    def __str__(self):
        return f'Сессия пользователя: {self.user.username} - Активность: {self.is_active}'

    class Meta:
        verbose_name = 'Сессия'
        verbose_name = 'Сессии'


class RefreshToken(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='refresh_token')
    token = models.CharField(max_length=550)
    duration = models.DurationField(default=week)

    def __str__(self):
        return f'Refresh token {self.pk}'

    class Meta:
        verbose_name = 'Refresh token'
        verbose_name = 'Refresh token'


