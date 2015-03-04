# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_user', '0002_auto_20150304_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerprofile',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='imager_user.ImagerProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='picture',
            field=models.ImageField(upload_to=b'imager_user', blank=True),
            preserve_default=True,
        ),
    ]
