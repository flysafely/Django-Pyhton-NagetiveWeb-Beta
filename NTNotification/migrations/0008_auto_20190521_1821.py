# Generated by Django 2.0.6 on 2019-05-21 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTNotification', '0007_auto_20190521_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attitudenotification',
            old_name='CObject',
            new_name='Comment',
        ),
        migrations.RenameField(
            model_name='attitudenotification',
            old_name='TObject',
            new_name='Topic',
        ),
    ]