# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0003_auto_20180129_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerinfo',
            name='category',
            field=models.CharField(blank=True, choices=[('3JUN', '3 юношеский'), ('2JUN', '2 юношеский'), ('1JUN', '1 юношеский'), ('3ADU', '3 взрослый'), ('2ADU', '2 взрослый'), ('1ADU', '1 взрослый'), ('KMS', 'Кандидат в мастера спорта'), ('MS', 'Мастер спорта'), ('MSI', 'Мастер спорта международного класса')], max_length=4, null=True),
        ),
    ]
