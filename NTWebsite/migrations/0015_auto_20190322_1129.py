# Generated by Django 2.0.6 on 2019-03-22 03:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0014_auto_20190321_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentinfo',
            name='TopicID',
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='CommentID',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='评论ID'),
        ),
        migrations.AlterField(
            model_name='commentinfo',
            name='ObjectID',
            field=models.CharField(default='', max_length=100, verbose_name='文章ID'),
        ),
    ]
