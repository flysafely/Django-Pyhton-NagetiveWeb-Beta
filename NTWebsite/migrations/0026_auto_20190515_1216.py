# Generated by Django 2.0.6 on 2019-05-15 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0025_auto_20190514_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rollcallinfo',
            name='Collect',
            field=models.IntegerField(default=0, verbose_name='围观度'),
        ),
        migrations.AlterField(
            model_name='rollcallinfo',
            name='Comment',
            field=models.IntegerField(default=0, verbose_name='互动数'),
        ),
        migrations.AlterField(
            model_name='rollcallinfo',
            name='Hot',
            field=models.IntegerField(default=0, verbose_name='热度'),
        ),
        migrations.AlterField(
            model_name='rollcallinfo',
            name='Share',
            field=models.IntegerField(default=0, verbose_name='分享数'),
        ),
    ]