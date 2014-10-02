# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'mentor_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, primary_key=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('short_bio', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'mentor', ['UserProfile'])

        # Adding model 'EducationDetails'
        db.create_table(u'mentor_educationdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mentor.UserProfile'])),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('branch', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('from_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('to_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'mentor', ['EducationDetails'])

        # Adding model 'SocialProfiles'
        db.create_table(u'mentor_socialprofiles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.OneToOneField')(related_name='social_profiles', unique=True, to=orm['mentor.UserProfile'])),
            ('profile_url_facebook', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('profile_url_linkedin', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('profile_url_twitter', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('profile_pic_url_facebook', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('profile_pic_url_linkedin', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('profile_pic_url_twitter', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'mentor', ['SocialProfiles'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'mentor_userprofile')

        # Deleting model 'EducationDetails'
        db.delete_table(u'mentor_educationdetails')

        # Deleting model 'SocialProfiles'
        db.delete_table(u'mentor_socialprofiles')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mentor.educationdetails': {
            'Meta': {'object_name': 'EducationDetails'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'from_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mentor.UserProfile']"}),
            'to_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'mentor.socialprofiles': {
            'Meta': {'object_name': 'SocialProfiles'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'social_profiles'", 'unique': 'True', 'to': u"orm['mentor.UserProfile']"}),
            'profile_pic_url_facebook': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'profile_pic_url_linkedin': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'profile_pic_url_twitter': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'profile_url_facebook': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'profile_url_linkedin': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'profile_url_twitter': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'mentor.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'short_bio': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['mentor']