# Generated by Django 2.0.6 on 2019-03-21 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0013_auto_20190321_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='User',
            new_name='Publisher',
        ),
        migrations.RenameField(
            model_name='tipoffbox',
            old_name='User',
            new_name='Publisher',
        ),
    ]
