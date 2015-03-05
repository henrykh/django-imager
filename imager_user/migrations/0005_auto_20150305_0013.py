# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_user', '0004_imagerprofile_blocking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagerprofile',
            old_name='following',
            new_name='follows',
        ),
    ]
