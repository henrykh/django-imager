# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('imager_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Number must be in the format: '+999999999'. Up to 15 digits")]),
            preserve_default=True,
        ),
    ]
