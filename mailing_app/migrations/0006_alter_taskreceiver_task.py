# Generated by Django 5.2 on 2025-04-18 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0005_remove_taskreceiver_received_taskreceiver_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskreceiver',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receivers', to='mailing_app.task', verbose_name='Задача'),
        ),
    ]
