# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_user', '0003_auto_20150304_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerprofile',
            name='blocking',
            field=models.ManyToManyField(related_name='blocked', to='imager_user.ImagerProfile'),
            preserve_default=True,
        ),
    ]
