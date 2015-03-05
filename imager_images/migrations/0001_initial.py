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
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('date_uploaded', models.DateField(null=True, blank=True)),
                ('date_modified', models.DateField(null=True, blank=True)),
                ('date_published', models.DateField(null=True, blank=True)),
                ('published', models.CharField(default=b'pvt', max_length=3, choices=[(b'pvt', b'Private'), (b'shd', b'Shared'), (b'pub', b'Public')])),
                ('user', models.ForeignKey(related_name='albums', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('date_uploaded', models.DateField(null=True, blank=True)),
                ('date_modified', models.DateField(null=True, blank=True)),
                ('date_published', models.DateField(null=True, blank=True)),
                ('published', models.CharField(default=b'pvt', max_length=3, choices=[(b'pvt', b'Private'), (b'shd', b'Shared'), (b'pub', b'Public')])),
                ('albums', models.ManyToManyField(related_name='photos', to='imager_images.Album')),
                ('user', models.ForeignKey(related_name='photos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
