# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager', '0002_auto_20150303_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
