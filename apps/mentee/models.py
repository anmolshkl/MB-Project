from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MenteeProfile(models.Model):

    """Associates the User with a 'Profile'."""

    # Stores username, password, first_name, last_name, email
    user = models.OneToOneField(User, related_name="mentee_profile", editable=False,
                                primary_key=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')
    date_of_birth = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True)
    college = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    about = models.CharField(max_length=256, blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)


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
            profile = MenteeProfile.objects.create(user=instance)

    models.signals.post_save.connect(create_user_profile, sender=User)


class SocialProfiles(models.Model):
    """Stores social profile urls of the user"""

    parent = models.OneToOneField(MenteeProfile, related_name="social_profiles",
                                  editable=False)
    #we may need other social urls for later use
    profile_url_facebook = models.URLField(max_length=256, blank=True)
    profile_url_linkedin = models.URLField(max_length=256, blank=True)
    profile_url_twitter  = models.URLField(max_length=256, blank=True)
    profile_pic_url_facebook = models.URLField(max_length=256, blank=True)
    profile_pic_url_linkedin = models.URLField(max_length=256, blank=True)
    profile_pic_url_twitter  = models.URLField(max_length=256, blank=True)

    def __unicode__(self):
        return u"Social Profiles - {0}".format(self.parent.full_name())

    class Meta:
        verbose_name = verbose_name_plural = "Social Profiles"
