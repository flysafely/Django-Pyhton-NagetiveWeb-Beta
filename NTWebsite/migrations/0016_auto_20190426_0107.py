# Generated by Django 2.0.6 on 2019-04-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0015_auto_20190322_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configparams',
            name='AvatarSavePath',
            field=models.CharField(default='Avatar/', max_length=50, verbose_name='头像存放路径'),
        ),
        migrations.AlterField(
            model_name='configparams',
            name='DefaultAvatar',
            field=models.ImageField(blank=True, default='', upload_to='Avatar', verbose_name='默认头像'),
        ),
    ]