# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0010_remove_photo_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='file_size',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
