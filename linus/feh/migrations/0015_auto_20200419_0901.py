# Generated by Django 2.2.10 on 2020-04-19 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feh', '0014_auto_20200416_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='gender',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hero',
            name='is_dancer',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
