# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tournaments.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField(blank=True, default='', max_length=500)),
                ('type', models.CharField(choices=[('1', 'Только для обладателей клубной лицензии'), ('2', 'Только для обладателей игровой лицензии'), ('3', 'Для обладателей любой лицензии'), ('4', 'Публичный')], max_length=1)),
                ('games', models.IntegerField(default=1, verbose_name='amount of games in the tournament')),
                ('photo', models.ImageField(blank=True, upload_to=tournaments.models.filename)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayerInfo')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='tournament',
            name='players',
            field=models.ManyToManyField(through='tournaments.TournamentMembership', to='accounts.PlayerInfo'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='team_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.TeamType'),
        ),
    ]
