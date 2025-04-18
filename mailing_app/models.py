from django.db import models

from jwtapp.models import User

# Create your models here.


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задачи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения задачи')

    created_by = models.ForeignKey(User, verbose_name='Автор задачи', related_name='tasks', 
                                   on_delete=models.SET_NULL, null=True)
    updated_by = models.IntegerField(verbose_name='Кто изменил задачу', blank=True, null=True)

    title = models.CharField(verbose_name='Название задачи')
    message = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(verbose_name='Дата выполнения задачи')
    completed = models.BooleanField(default=False, verbose_name='Задача выполнена')

    def __str__(self):
        return f'Задача {self.pk}'
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class TaskReceiver(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='receivers', verbose_name='Задача')
    user = models.ForeignKey(on_delete=models.SET_NULL, null=True, verbose_name='Пользователь', to=User)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return f'Получатель {self.user.username} {self.user.pk}'
    
    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class TaskReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='reports')
    task_compeleted = models.BooleanField(default=False, verbose_name='Задача выполнена')
    total_receivers = models.IntegerField(verbose_name='Общее кол-во получателей')
    successful = models.IntegerField(verbose_name='Успешные')
    unsuccessful = models.IntegerField(verbose_name='Неуспешно')
    
    def __str__(self):
        return f'Отчёт по задаче {self.task.pk}'
    
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'