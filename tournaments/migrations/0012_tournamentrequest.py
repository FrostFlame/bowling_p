# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180407_1727'),
        ('tournaments', '0011_auto_20180407_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(0, 'In progress'), (1, 'Accepted'), (2, 'Declined')], default=0, max_length=1)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayerInfo')),
            ],
        ),
    ]
