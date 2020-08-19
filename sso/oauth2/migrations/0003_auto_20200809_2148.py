# Generated by Django 3.0.8 on 2020-08-09 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2', '0002_auto_20200807_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='domain',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('domain',)},
        ),
        migrations.RemoveField(
            model_name='client',
            name='company',
        ),
    ]
