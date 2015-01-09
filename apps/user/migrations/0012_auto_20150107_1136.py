# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20141224_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='resume',
            field=models.FileField(null=True, upload_to=apps.user.models.PathAndRename(b'resume/'), blank=True),
            preserve_default=True,
        ),
    ]
