# Generated by Django 2.0.9 on 2020-03-22 07:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('feh', '0004_auto_20200322_0737_squashed_0005_auto_20200322_0737'), ('feh', '0005_auto_20200322_0742')]

    dependencies = [
        ('feh', '0003_auto_20200317_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='pullable_3star',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='pullable_4star',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='pullable_5star',
        ),
        migrations.AddField(
            model_name='hero',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None),
        ),
        migrations.AddField(
            model_name='hero',
            name='rarities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hero',
            name='availability',
            field=models.CharField(choices=[('STANDARD', 'Standard Pool'), ('SPECIAL', 'Limited Hero'), ('GHB', 'Grand Hero Battle'), ('TT', 'Tempest Trials'), ('LEGENDARY', 'Legendary Hero'), ('MYTHIC', 'Mythic Hero'), ('STORY', 'Story Hero'), ('DUO', 'Duo')], max_length=15),
        ),
    ]