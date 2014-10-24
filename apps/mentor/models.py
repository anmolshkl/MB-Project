from django.db import models
from django.contrib.auth.models import User

# for django-allauth signals
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up

from apps.user.models import UserProfile
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

