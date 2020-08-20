# Generated by Django 3.0.8 on 2020-08-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2', '0003_auto_20200809_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email_key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='photo_url_key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='profile_url_key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]