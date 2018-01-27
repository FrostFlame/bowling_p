# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 12:07
from __future__ import unicode_literals

import Auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_auto_20180126_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerinfo',
            name='passport',
            field=models.ImageField(blank=True, upload_to=Auth.models.user_folder),
        ),
        migrations.AlterField(
            model_name='playerinfo',
            name='sex',
            field=models.CharField(choices=[('0', 'Мужской'), ('1', 'Женский')], max_length=1, null=True),
        ),
    ]
