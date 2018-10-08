# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-21 13:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tournaments.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180920_1510'),
        ('tournaments', '0014_auto_20180424_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.TextField(blank=True, default='', max_length=500)),
                ('is_final', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BlockType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Типы блоков',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('players', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayerInfo')),
            ],
        ),
        migrations.RemoveField(
            model_name='tournamentmembership',
            name='player',
        ),
        migrations.RemoveField(
            model_name='tournamentmembership',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='tournamentrequest',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='tournamentrequest',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name_plural': 'Игры'},
        ),
        migrations.AlterModelOptions(
            name='teamtype',
            options={'verbose_name_plural': 'Типы команд'},
        ),
        migrations.AlterModelOptions(
            name='tournament',
            options={'verbose_name_plural': 'Турниры'},
        ),
        migrations.RenameField(
            model_name='gameinfo',
            old_name='result',
            new_name='point',
        ),
        migrations.RemoveField(
            model_name='game',
            name='players',
        ),
        migrations.RemoveField(
            model_name='game',
            name='start',
        ),
        migrations.RemoveField(
            model_name='game',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='gameinfo',
            name='player',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='players',
        ),
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AddField(
            model_name='game',
            name='is_desperado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='tournament',
            name='handicap',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='handicap_size',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='tournaments.Game'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='photo',
            field=models.ImageField(blank=True, default='default\\tournament_avatar.png', upload_to=tournaments.models.filename),
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='team_type',
        ),
        migrations.AddField(
            model_name='tournament',
            name='team_type',
            field=models.ManyToManyField(to='tournaments.TeamType'),
        ),
        migrations.DeleteModel(
            name='TournamentMembership',
        ),
        migrations.DeleteModel(
            name='TournamentRequest',
        ),
        migrations.AddField(
            model_name='team',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_tournament', to='tournaments.Tournament'),
        ),
        migrations.AddField(
            model_name='block',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_tournament', to='tournaments.Tournament'),
        ),
        migrations.AddField(
            model_name='block',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_type', to='tournaments.BlockType'),
        ),
        migrations.AddField(
            model_name='game',
            name='block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='block', to='tournaments.Block'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='tournaments.Team'),
            preserve_default=False,
        ),
    ]