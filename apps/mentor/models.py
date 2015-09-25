from django.db import models
from django.contrib.auth.models import User

# for django-allauth signals
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up

from apps.user.models import UserProfile


# Create your models here.
class EducationDetails(models.Model):
    """Stores educational details of the user"""

    parent = models.ForeignKey(UserProfile, related_name='education_details', editable=False)
    institution = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True)
    degree = models.CharField(max_length=64, blank=True)
    branch = models.CharField(max_length=256, blank=True)
    from_year = models.IntegerField(blank=True, null=True)
    to_year = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'{1} from {0}'.format(self.institution, self.branch)

    class Meta:
        verbose_name = verbose_name_plural = "Educational Details"


class EmploymentDetails(models.Model):
    """Stores employment details of the user"""

    parent = models.ForeignKey(UserProfile, related_name='employment_details', blank=False)
    organization = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    position = models.CharField(max_length=256, blank=True)
    from_year = models.IntegerField(blank=True, null=True)
    to_year = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.organization)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name = verbose_name_plural = "Employment Details"


class UserActivity(models.Model):
    mentor = models.OneToOneField(User, editable=False, related_name="activity", primary_key=True)
    last_seen = models.DateTimeField(blank=False, null=True)

    def __unicode__(self):
        return u'{}'.format(self.mentor)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Activities"


class Timings(models.Model):
    parent = models.OneToOneField(User, related_name="timings", primary_key=True)
    weekday_l = models.CharField(max_length=5, blank=False, null=False)
    weekday_u = models.CharField(max_length=5, blank=False, null=False)
    weekend_l = models.CharField(max_length=5, blank=False, null=False)
    weekend_u = models.CharField(max_length=5, blank=False, null=False)

    def __unicode__(self):
        return u'{}'.format(self.parent)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Timings"


class Ratings(models.Model):
    mentor = models.OneToOneField(User, related_name="ratings", primary_key=True)
    count = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    one = models.IntegerField(max_length=1, default=0)
    two = models.IntegerField(max_length=1, default=0)
    three = models.IntegerField(max_length=1, default=0)
    four = models.IntegerField(max_length=1, default=0)
    five = models.IntegerField(max_length=1, default=0)

    def __unicode__(self):
        return u'{}'.format(self.mentor)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Ratings"

class Business_categories(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35, blank=False, null=False)

    def __unicode__(self):
        return u'{}'.format(self.id,self.name)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Business Categories"

class Business_subcategories(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35, blank=False, null=False)
    category = models.ForeignKey(Business_categories, editable=False)

    def __unicode__(self):
        return u'{}'.format(self.id,self.name,self.category)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Business Subcategories"

class Business_Mentor_Tags(models.Model):
    mentor = models.ForeignKey(User, limit_choices_to={'is_bmentor': True})
    subcategory = models.ForeignKey(Business_subcategories)

    def __unicode__(self):
        return u'{}'.format(self.mentor,self.subcategory)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name_plural = "Business Mentor Tags"


