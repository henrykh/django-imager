# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday_privacy',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='email_privacy',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='name_privacy',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_privacy',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture_privacy',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
