# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialProfiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_url_facebook', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_url_linkedin', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_url_twitter', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_url_google', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_url_github', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_pic_url_facebook', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_pic_url_linkedin', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_pic_url_google', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_pic_url_github', models.URLField(default=b'', max_length=256, blank=True)),
                ('profile_pic_url_twitter', models.URLField(default=b'', max_length=256, blank=True)),
            ],
            options={
                'verbose_name': 'Social Profiles',
                'verbose_name_plural': 'Social Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name=b'user_profile', primary_key=True, serialize=False, editable=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(default=b'M', max_length=1, blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('contact', models.CharField(max_length=128, blank=True)),
                ('college', models.CharField(max_length=128, blank=True)),
                ('city', models.CharField(max_length=128, blank=True)),
                ('state', models.CharField(max_length=128, blank=True)),
                ('country', models.CharField(max_length=128, blank=True)),
                ('about', models.TextField(blank=True)),
                ('resume', models.FileField(null=True, upload_to=apps.user.models.PathAndRename(b'resume/'), blank=True)),
                ('picture', models.CharField(max_length=128, null=True, blank=True)),
                ('is_mentor', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='socialprofiles',
            name='parent',
            field=models.OneToOneField(related_name=b'social_profiles', editable=False, to='user.UserProfile'),
            preserve_default=True,
        ),
    ]
