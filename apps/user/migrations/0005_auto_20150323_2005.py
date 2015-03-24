# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20150323_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='rid',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
