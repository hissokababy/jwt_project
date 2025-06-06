# Generated by Django 5.2 on 2025-04-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Номер телефона'),
        ),
    ]
