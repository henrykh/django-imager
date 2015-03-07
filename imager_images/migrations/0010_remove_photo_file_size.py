# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0009_auto_20150306_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='file_size',
        ),
    ]
