# Generated by Django 2.2.19 on 2021-03-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210327_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(verbose_name='Адрес'),
        ),
    ]
