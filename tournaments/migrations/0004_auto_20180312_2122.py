# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import tournaments.models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20180312_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='photo',
            field=models.ImageField(blank=True, default='default/tournament_avatar.png', upload_to=tournaments.models.filename),
        ),
    ]
