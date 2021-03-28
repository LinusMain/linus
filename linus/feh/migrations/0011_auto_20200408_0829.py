# Generated by Django 2.2.10 on 2020-04-08 08:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feh', '0010_auto_20200408_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='movement_permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('M_01_INFANTRY', 'Infantry'), ('M_04_ARMOR', 'Armor'), ('M_02_FLYING', 'Flying'), ('M_03_CAVALRY', 'Cavalry')], max_length=15), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='weapon_permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('W_01_SWORD', 'R Sword'), ('W_02_LANCE', 'B Lance'), ('W_03_AXE', 'G Axe'), ('W_11_R_TOME', 'R Tome'), ('W_12_B_TOME', 'B Tome'), ('W_13_G_TOME', 'G Tome'), ('W_14_C_TOME', 'C Tome'), ('W_15_X_TOME', 'X Tome'), ('W_21_R_BOW', 'R Bow'), ('W_22_B_BOW', 'B Bow'), ('W_23_G_BOW', 'G Bow'), ('W_24_C_BOW', 'C Bow'), ('W_25_X_BOW', 'X Bow'), ('W_31_R_DAGGER', 'R Dagger'), ('W_32_B_DAGGER', 'B Dagger'), ('W_33_G_DAGGER', 'G Dagger'), ('W_34_C_DAGGER', 'C Dagger'), ('W_35_X_DAGGER', 'X Dagger'), ('W_41_R_DRAGON', 'R Dragon'), ('W_42_B_DRAGON', 'B Dragon'), ('W_43_G_DRAGON', 'G Dragon'), ('W_44_C_DRAGON', 'C Dragon'), ('W_45_X_DRAGON', 'X Dragon'), ('W_51_R_BEAST', 'R Beast'), ('W_52_B_BEAST', 'B Beast'), ('W_53_G_BEAST', 'G Beast'), ('W_54_C_BEAST', 'C Beast'), ('W_55_X_BEAST', 'X Beast'), ('W_64_C_STAFF', 'C Staff'), ('W_65_X_STAFF', 'X Staff'), ('W_71_ASSIST', 'Assist'), ('W_81_SPECIAL', 'Special'), ('W_91_A', 'A'), ('W_91_A', 'B'), ('W_91_A', 'C'), ('W_94_SS', 'Sacred Seal')], max_length=15), default=[], size=None),
            preserve_default=False,
        ),
    ]