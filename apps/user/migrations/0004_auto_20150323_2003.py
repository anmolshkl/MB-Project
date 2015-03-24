# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150323_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='id',
        ),
        migrations.AddField(
            model_name='request',
            name='rid',
            field=models.IntegerField(default=None, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
