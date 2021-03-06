# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='text',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
