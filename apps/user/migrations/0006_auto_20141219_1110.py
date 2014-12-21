# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20141218_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=apps.user.models.PathAndRename(b'/media/profile_images'), blank=True),
        ),
    ]
