# Generated by Django 2.0.6 on 2019-05-06 03:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0018_auto_20190506_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicinfo',
            name='CreateTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间'),
        ),
    ]
