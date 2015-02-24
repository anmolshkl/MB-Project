# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution', models.CharField(max_length=128, blank=True)),
                ('location', models.CharField(max_length=128, blank=True)),
                ('degree', models.CharField(max_length=64, blank=True)),
                ('branch', models.CharField(max_length=256, blank=True)),
                ('from_year', models.IntegerField(max_length=4, null=True, blank=True)),
                ('to_year', models.IntegerField(max_length=4, null=True, blank=True)),
                ('country', models.CharField(max_length=128, blank=True)),
                ('parent', models.ForeignKey(editable=False, to='user.UserProfile')),
            ],
            options={
                'verbose_name': 'Educational Details',
                'verbose_name_plural': 'Educational Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmploymentDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.CharField(max_length=128, blank=True)),
                ('location', models.CharField(max_length=128, blank=True)),
                ('position', models.CharField(max_length=256, blank=True)),
                ('from_date', models.DateField(null=True, blank=True)),
                ('to_date', models.DateField(null=True, blank=True)),
                ('parent', models.ForeignKey(editable=False, to='user.UserProfile')),
            ],
            options={
                'verbose_name': 'Employment Details',
                'verbose_name_plural': 'Employment Details',
            },
            bases=(models.Model,),
        ),
    ]
