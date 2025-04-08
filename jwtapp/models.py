from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(AbstractUser):
#     ...

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', blank=True, null=True)

    class Meta:
        abstract = True


class Session(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name='Пользователь')
    user_ip = models.GenericIPAddressField(max_length=155, verbose_name='Ip устройства пользователя', blank=True, null=True, unique=True)
    refresh_token = models.CharField(max_length=550, verbose_name='Refresh token', blank=True, null=True)
    device_type = models.CharField(max_length=150, verbose_name='Тип устройства', blank=True, null=True, default='mobile')
    active = models.BooleanField(default=True, verbose_name='Активная сессия')

    def __str__(self):
        return f'Сессия пользователя: {self.user.username} | {self.active}'

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

