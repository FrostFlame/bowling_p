# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0012_tournamentrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
