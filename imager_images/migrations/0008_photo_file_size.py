# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0007_auto_20150306_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='file_size',
            field=models.CharField(max_length=100, null=True, verbose_name=b'image__file__size', blank=True),
            preserve_default=True,
        ),
    ]
