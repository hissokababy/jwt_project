from django.db import models

from jwtapp.models import User

# Create your models here.


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задачи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения задачи')

    created_by = models.ForeignKey(User, verbose_name='Автор задачи', 
                                   on_delete=models.SET_NULL, null=True, related_name='tasks')
    updated_by = models.ForeignKey(User, verbose_name='Кто изменил задачу', 
                                   on_delete=models.SET_NULL, null=True)

    title = models.CharField(verbose_name='Название задачи', blank=True, null=True, max_length=500)
    message = models.TextField(verbose_name='Текст', blank=True, null=True)
    date = models.DateTimeField(verbose_name='Дата выполнения задачи', blank=True, null=True)
    completed = models.BooleanField(default=False, verbose_name='Задача выполнена')

    def __str__(self):
        return f'Задача {self.pk}'
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskReceiver(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='receivers', verbose_name='Задача')
    user = models.ForeignKey(on_delete=models.SET_NULL, null=True, verbose_name='Пользователь', to=User)

    def __str__(self):
        return f'Получатель {self.user.username} {self.user.pk}'
    
    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class TaskReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='reports')
    task_compeleted = models.BooleanField(default=False, verbose_name='Задача выполнена')
    total_receivers = models.PositiveIntegerField(verbose_name='Общее кол-во получателей')
    successful = models.PositiveIntegerField(verbose_name='Успешные')
    error_detail = models.CharField(verbose_name='Описание ошибки', blank=True, null=True, max_length=500)
    
    def __str__(self):
        return f'Отчёт №{self.pk} по задаче {self.task.pk}'
    
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'