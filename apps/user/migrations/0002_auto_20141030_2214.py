# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofiles',
            name='profile_pic_url_github',
            field=models.URLField(default=b'', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofiles',
            name='profile_pic_url_google',
            field=models.URLField(default=b'', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofiles',
            name='profile_url_github',
            field=models.URLField(default=b'', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofiles',
            name='profile_url_google',
            field=models.URLField(default=b'', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_pic_url_facebook',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_pic_url_linkedin',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_pic_url_twitter',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_url_facebook',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_url_linkedin',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='socialprofiles',
            name='profile_url_twitter',
            field=models.URLField(default=b'', max_length=256, blank=True),
        ),
    ]
