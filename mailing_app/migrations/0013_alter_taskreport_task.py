# Generated by Django 5.2 on 2025-04-19 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0012_alter_taskreport_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskreport',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='mailing_app.task'),
        ),
    ]
