# Generated by Django 2.2.10 on 2020-04-08 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feh', '0009_auto_20200408_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='book',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
