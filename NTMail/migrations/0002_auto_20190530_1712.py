# Generated by Django 2.0.6 on 2019-05-30 09:12

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTMail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbody',
            name='Html',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='邮件HTML'),
        ),
    ]