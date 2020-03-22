# Generated by Django 2.0.9 on 2020-03-15 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feh', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='book',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hero',
            name='generation',
            field=models.IntegerField(default=1, verbose_name='gen'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hero',
            name='release_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hero',
            name='attack',
            field=models.IntegerField(verbose_name='atk'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='bst',
            field=models.IntegerField(verbose_name='BST'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='defense',
            field=models.IntegerField(verbose_name='def'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='is_f2p',
            field=models.BooleanField(verbose_name='f2p'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='resistance',
            field=models.IntegerField(verbose_name='res'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='speed',
            field=models.IntegerField(verbose_name='spd'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='weapon_type',
            field=models.CharField(choices=[('SWORD', 'R Sword'), ('LANCE', 'B Lance'), ('AXE', 'G Axe'), ('R_TOME', 'R Tome'), ('B_TOME', 'B Tome'), ('G_TOME', 'G Tome'), ('C_TOME', 'C Tome'), ('R_BOW', 'R Bow'), ('B_BOW', 'B Bow'), ('G_BOW', 'G Bow'), ('C_BOW', 'C Bow'), ('R_DAGGER', 'R Dagger'), ('B_DAGGER', 'B Dagger'), ('G_DAGGER', 'G Dagger'), ('C_DAGGER', 'C Dagger'), ('R_DRAGON', 'R Dragon'), ('B_DRAGON', 'B Dragon'), ('G_DRAGON', 'G Dragon'), ('C_DRAGON', 'C Dragon'), ('R_BEAST', 'R Beast'), ('B_BEAST', 'B Beast'), ('G_BEAST', 'G Beast'), ('C_BEAST', 'C Beast'), ('C_STAFF', 'C Staff')], max_length=15),
        ),
    ]