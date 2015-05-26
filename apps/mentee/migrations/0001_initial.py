# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('parent', models.OneToOneField(related_name=b'credits', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('balance', models.FloatField(default=5.0, blank=True)),
            ],
            options={
                'verbose_name': 'Credits',
                'verbose_name_plural': 'Credits',
            },
            bases=(models.Model,),
        ),
    ]
