# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20141219_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(upload_to=apps.user.models.PathAndRename(b'profile_images/'), blank=True),
        ),
    ]
