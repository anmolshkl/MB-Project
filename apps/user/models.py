from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# for django-allauth signals
from allauth.account.signals import user_logged_in, user_signed_up
import datetime

# for upload_to
from django.utils import timezone

from django.utils.deconstruct import deconstructible
from mentorbuddy import settings
import os

from haystack.forms import SearchForm

import apps.user.fields

# http://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(instance.user.username, ext)
        # return the whole path to the file
        newPath = os.path.join(settings.MEDIA_ROOT, "resume")
        if not os.path.exists(newPath):
            os.makedirs(newPath)

        return os.path.join(newPath, instance.user.username + "." + ext)


path_and_rename = PathAndRename("/resume/")


class UserProfile(models.Model):
    @staticmethod
    def generate_new_filename(instance, filename):
        f, ext = os.path.splitext(filename)
        return '%s%s' % (instance.user.username, ext)

    """Associates the User with a 'Profile'."""

    # Stores username, password, first_name, last_name, email
    user = models.OneToOneField(User, related_name="user_profile", editable=False,
                                primary_key=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True)
    college = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    about = models.TextField(blank=True)
    resume = models.FileField(upload_to=path_and_rename, null=True, blank=True)
    picture = models.CharField(max_length=256, default='/static/img/no-profile-pic.jpg')  # Contains URL
    is_mentor = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    timezone = models.CharField(max_length=256, null=True, default=None)

    def full_name(self):
        return self.user.get_full_name()

    def __unicode__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        else:
            return self.user.username

    class Meta:
        verbose_name = "User Profile"

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile.objects.create(user=instance)


    models.signals.post_save.connect(create_user_profile, sender=User)


class SocialProfiles(models.Model):
    """Stores social profile urls of the user"""

    parent = models.OneToOneField(UserProfile, related_name="social_profiles",
                                  editable=False)
    # we may need other social urls for later use
    profile_url_facebook = models.URLField(max_length=256, blank=True, default='')
    profile_url_linkedin = models.URLField(max_length=256, blank=True, default='')
    profile_url_twitter = models.URLField(max_length=256, blank=True, default='')
    profile_url_google = models.URLField(max_length=256, blank=True, default='')
    profile_url_github = models.URLField(max_length=256, blank=True, default='')

    profile_pic_url_facebook = models.URLField(max_length=256, blank=True, default='')
    profile_pic_url_linkedin = models.URLField(max_length=256, blank=True, default='')
    profile_pic_url_google = models.URLField(max_length=256, blank=True, default='')
    profile_pic_url_github = models.URLField(max_length=256, blank=True, default='')
    profile_pic_url_twitter = models.URLField(max_length=256, blank=True, default='')

    def __unicode__(self):
        return u"Social Profiles - {0}".format(self.parent.full_name())

    class Meta:
        verbose_name = verbose_name_plural = "Social Profiles"


# Create your models here.@receiver ([user_signed_up, user_logged_in], sender=User)
@receiver([user_signed_up, user_logged_in])
def save_data(sender, **kwargs):
    ''' 
    things to do:
                1.create social profile for the user and populate it 
                2.let the adapter do its work of returning different login urls->dont need this now
    '''
    user = kwargs.pop('user')
    userProfile, usrprof_created = UserProfile.objects.get_or_create(user=user)
    socialProfiles, socprof_created = SocialProfiles.objects.get_or_create(parent=userProfile)

    # try to check whether user has any data provided by LinkedIn
    extra_data = None
    try:
        extra_data = user.socialaccount_set.filter(provider='linkedin')[0].extra_data
    except:
        pass
    if extra_data:
        # Save user's social profile image everytime he logs in/hardcode for LinkedIn
        userProfile.picture = extra_data['picture-url']
        userProfile.email_verified = True
        userProfile.save()
        socialProfiles.profile_url_linkedin = extra_data['public-profile-url']
        socialProfiles.profile_pic_url_linkedin = extra_data['picture-url']
        socialProfiles.save()

    extra_data = None
    try:
        extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    except:
        pass
    if extra_data:
        # Save user's social profile image everytime he logs in/hardcode for facebook
        userProfile.picture = "http://graph.facebook.com/" + user.socialaccount_set.filter(provider='facebook')[
            0].uid + "/picture?type=large"
        userProfile.email_verified = True
        userProfile.save()
        socialProfiles.profile_url_facebook = extra_data['link']
        socialProfiles.profile_pic_url_facebook = userProfile.picture
        socialProfiles.save()


class MentorSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        # First, store the SearchQuerySet received from other processing. (the main work is run internally by Haystack here).
        sqs = super(MentorSearchForm, self).search()

        # if something goes wrong
        if not self.is_valid():
            return self.no_query_found()

        # you can then adjust the search results and ask for instance to order the results by title
        # sqs = sqs.order_by(city)

        return sqs


class Request(models.Model):
    menteeId = models.ForeignKey(User, related_name="requestsMade", blank=False)
    mentorId = models.ForeignKey(User, related_name="requestsReceived", blank=False)
    dateTime = models.DateTimeField(blank=False, default=datetime.datetime.now)
    # time = models.TimeField(blank=False, default=datetime.datetime.now)
    duration = apps.user.fields.IntegerRangeField(min_value=1, max_value=30)
    is_approved = models.NullBooleanField(default=None, null=True)
    is_rescheduled = models.BooleanField(default=False)
    requestDate = models.DateField(blank=False, default=datetime.date.today)
    callType = apps.user.fields.IntegerRangeField(min_value=1, max_value=3, default=1)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Request"

    def __unicode__(self):
        request_name = User.objects.get(id=self.menteeId_id).first_name + " to " + User.objects.get(
            id=self.mentorId_id).first_name + " for " + str(self.dateTime.date())
        if request_name:
            return request_name
        else:
            return self.id


class CallLog(models.Model):
    request = models.OneToOneField(Request, related_name="callLog", primary_key=True)
    establishedTime = models.TimeField(blank=False, default=datetime.datetime.now)
    endTime = models.TimeField(blank=False, default=datetime.datetime.now)
    duration = apps.user.fields.IntegerRangeField(default=0, min_value=5, max_value=30, verbose_name="Duration(sec)")
    endCause = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Call Log"

    def __unicode__(self):
        request_name = User.objects.get(id=self.request.menteeId_id).first_name + " to " + User.objects.get(
            id=self.request.mentorId_id).first_name + " on " + str(self.request.dateTime.date().strftime("%d-%m-%y"))
        if request_name:
            return request_name
        else:
            return self.id


class Feedback(models.Model):
    """"Stores Feedback for every call """""
    user = models.ForeignKey(User, editable=False)
    call = models.ForeignKey(CallLog, editable=False)
    rating = models.FloatField(null=False, default=0.0, blank=False)
    feedback = models.CharField(max_length=512, null=False, blank=True)

    class Meta:
        verbose_name = "Feedback"

    def __unicode__(self):
        user = self.user.get_full_name()
        return "from " + user


class VerificationCodes(models.Model):
    user = models.OneToOneField(User, related_name="verification", primary_key=True)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = u'VerificationCodes'


class Notification(models.Model):
    to = models.ForeignKey(User, related_name="notifications", editable=False)
    frm = models.CharField(User, editable=False, max_length=300)  # from is reserved keyword
    text = models.TextField(blank=True, max_length=300, null=True)
    title = models.CharField(blank=True, max_length=500, null=False)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.to

    class Meta:
        verbose_name_plural = u'Notifications'
