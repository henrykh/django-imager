# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0002_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_modified',
            field=models.DateField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='date_uploaded',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
