# Generated by Django 2.0.6 on 2019-03-05 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0009_rollcalldialogue_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rollcalldialogue',
            name='EditDate',
            field=models.DateTimeField(auto_now=True, verbose_name='编辑时间'),
        ),
        migrations.AlterField(
            model_name='rollcallinfo',
            name='EditDate',
            field=models.DateTimeField(auto_now=True, verbose_name='编辑时间'),
        ),
    ]
