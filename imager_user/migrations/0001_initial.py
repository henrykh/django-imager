# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'imager_user', blank=True)),
                ('picture_privacy', models.BooleanField(default=True)),
                ('phone_number', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Number must be in the format: '+999999999'. Up to 15 digits")])),
                ('phone_privacy', models.BooleanField(default=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('birthday_privacy', models.BooleanField(default=True)),
                ('name_privacy', models.BooleanField(default=True)),
                ('email_privacy', models.BooleanField(default=True)),
                ('blocking', models.ManyToManyField(related_name='blocked', to='imager_user.ImagerProfile', blank=True)),
                ('follows', models.ManyToManyField(related_name='followers', to='imager_user.ImagerProfile', blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
