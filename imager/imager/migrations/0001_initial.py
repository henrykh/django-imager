# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.FileField(upload_to=b'', blank=True)),
                ('picture_privacy', models.BooleanField(default=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('phone_privacy', models.BooleanField(default=True)),
                ('birthday', models.DateField()),
                ('birthday_privacy', models.BooleanField(default=True)),
                ('name_privacy', models.BooleanField(default=True)),
                ('email_privacy', models.BooleanField(default=True)),
                ('associated_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
