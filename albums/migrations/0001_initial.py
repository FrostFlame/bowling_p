# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-06 21:43
from __future__ import unicode_literals

import albums.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('cover', models.ImageField(upload_to=albums.models.album_cover_path)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('image', models.ImageField(upload_to=albums.models.album_image_path)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Album')),
            ],
        ),
    ]