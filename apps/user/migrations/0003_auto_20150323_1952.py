# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import apps.user.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_userprofile_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField(default=datetime.datetime.now)),
                ('duration', apps.user.fields.IntegerRangeField()),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rescheduled', models.BooleanField(default=False)),
                ('requestDate', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Request',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('request', models.OneToOneField(related_name=b'callLog', primary_key=True, serialize=False, to='user.Request')),
                ('establishedTime', models.TimeField(default=datetime.datetime.now)),
                ('endTime', models.TimeField(default=datetime.datetime.now)),
                ('duration', apps.user.fields.IntegerRangeField()),
                ('endCause', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Call Log',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='menteeId',
            field=models.ForeignKey(related_name=b'requestsMade', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='mentorId',
            field=models.ForeignKey(related_name=b'requestsReceived', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
