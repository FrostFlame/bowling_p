# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-07 14:27
from __future__ import unicode_literals

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_is_photographer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerinfo',
            name='avatar',
            field=models.ImageField(default='default\\player_avatar.png', upload_to=accounts.utils.UploadToPathAndRename('avatars/')),
        ),
    ]
