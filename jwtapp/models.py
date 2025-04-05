from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
week = datetime.timedelta(days=7)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name='Пользователь')
    user_ip = models.CharField(max_length=155, verbose_name='Ip устройства пользователя', blank=True, null=True)

    def __str__(self):
        return f'Сессия пользователя: {self.user.username} - Активность: {self.user.is_active}'

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'


class RefreshToken(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='refresh_token')
    token = models.CharField(max_length=550)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации токена', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления', blank=True, null=True)

    def __str__(self):
        return f'Refresh token {self.pk}'

    class Meta:
        verbose_name = 'Refresh token'
        verbose_name_plural = 'Refresh tokens'


