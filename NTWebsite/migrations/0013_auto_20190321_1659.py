# Generated by Django 2.0.6 on 2019-03-21 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0012_configparams_commonpagelimit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attitude',
            old_name='User',
            new_name='Publisher',
        ),
    ]
