from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name='Пользователь')
    user_ip = models.GenericIPAddressField(max_length=155, verbose_name='Ip устройства пользователя', blank=True, null=True)
    refresh_token = models.CharField(max_length=550, verbose_name='Refresh token', blank=True, null=True)


    def __str__(self):
        return f'Сессия пользователя: {self.user.username} - Активность: {self.user.is_active}'

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

