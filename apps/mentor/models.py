from django.db import models
from django.contrib.auth.models import User

# for django-allauth signals
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up

from apps.user.models import UserProfile

#for haystack
from haystack import indexes

# Create your models here.
class EducationDetails(models.Model):
    """Stores educational details of the user"""

    parent      = models.ForeignKey(UserProfile, editable=False)
    institution = models.CharField(max_length=128, blank=True)
    location    = models.CharField(max_length=128, blank=True)
    degree      = models.CharField(max_length=64,  blank=True)
    branch      = models.CharField(max_length=256, blank=True)
    from_year   = models.IntegerField(max_length=4, blank=True, null=True)
    to_year     = models.IntegerField(max_length=4, blank=True, null=True)
    country     = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return u'{1} from {0}'.format(self.institution, self.branch)

    class Meta:
        verbose_name = verbose_name_plural = "Educational Details"

class EmploymentDetails(models.Model):
    """Stores employment details of the user"""

    parent       = models.ForeignKey(UserProfile, editable=False)
    organization = models.CharField(max_length=128, blank=True)
    location     = models.CharField(max_length=128, blank=True)
    position     = models.CharField(max_length=256, blank=True)
    from_date    = models.DateField(blank=True, null=True)
    to_date      = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.organization)
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
            # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name = verbose_name_plural = "Employment Details"

class MentorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    college = indexes.CharField(model_attr='college')
    country = indexes.CharField(model_attr='country')
    
    def get_model(self):
        return UserProfile

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_mentor=True)