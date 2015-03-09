# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_auto_20150305_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='albums',
            field=models.ManyToManyField(related_name='photos', to='imager_images.Album', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_modified',
            field=models.DateField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_uploaded',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
