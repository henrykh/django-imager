# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager', '0003_auto_20150303_0338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagerprofile',
            old_name='associated_user',
            new_name='user',
        ),
    ]
