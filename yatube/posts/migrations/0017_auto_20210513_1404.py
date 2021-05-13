# Generated by Django 2.2.6 on 2021-05-13 11:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0016_auto_20210511_2307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
    ]
