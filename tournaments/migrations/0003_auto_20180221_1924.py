# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20180221_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='type',
            field=models.CharField(choices=[('C', 'CLUB LICENSE'), ('G', 'GAME LICENSE'), ('L', 'ANY LICENSE'), ('P', 'PUBLIC')], max_length=1),
        ),
    ]