# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20141219_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name=b'min_free_cropping',
            field=image_cropping.fields.ImageRatioField(b'picture', '200x200', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=True, adapt_rotation=False, help_text=None, verbose_name='min free cropping'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=image_cropping.fields.ImageCropField(null=True, upload_to=apps.user.models.PathAndRename(b'profile_images/'), blank=True),
        ),
    ]
