# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20141220_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name=b'min_free_cropping',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(null=True, upload_to=apps.user.models.PathAndRename(b'profile_images/'), blank=True),
        ),
    ]
