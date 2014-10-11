from django.db import models
from django.contrib.auth.models import User
# for django-allauth signals
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up

# Create your models here.
class MentorProfile(models.Model):

    """Associates the User with a 'Profile'."""

    # Stores username, password, first_name, last_name, email
    user = models.OneToOneField(User, related_name="mentor_profile", editable=False,
                                primary_key=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')
    date_of_birth = models.DateField(blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
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
            profile = MentorProfile.objects.create(user=instance)
            EducationDetails.objects.create(parent=profile)


    models.signals.post_save.connect(create_user_profile, sender=User)

class EducationDetails(models.Model):
    """Stores educational details of the user"""

    parent      = models.ForeignKey(MentorProfile, editable=False)
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

class SocialProfiles(models.Model):
    """Stores social profile urls of the user"""

    parent = models.OneToOneField(MentorProfile, related_name="social_profiles",
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


# Create your models here.@receiver ([user_signed_up, user_logged_in], sender=User)
@receiver([user_logged_in,user_signed_up])
def save_data(sender, **kwargs):
    user = kwargs.pop('user')
    #Populate database fields from provider extra_data for MENTOR
    extra_data = user.socialaccount_set.filter(provider='linkedin')[0].extra_data
    if extra_data:
        location = extra_data['location']['name']  #rename address as area
        first_name = extra_data['first-name']
        last_name = extra_data['last-name']
        user.first_name = first_name
        user.last_name = last_name
        (location,country) = location.split(',')
        #date_of_birth = extra_data['date-of-birth']  
        userProfile = MentorProfile(user=user)
        userProfile.location = location
        userProfile.country = country
        userProfile.save()
        user.save()

        socialProfile = SocialProfiles.objects.get(parent=userProfile)
        socialProfile.profile_url_linkedin = extra_data['public-profile-url']
        socialProfile.profile_pic_url_linkedin = extra_data['picture-url']
        socialProfile.save()
    extra_data = None
    extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    if extra_data:
        first_name = extra_data['first_name']
        last_name = extra_data['last_name']
        user.first_name = first_name
        user.last_name = last_name
        '''location = extra_data['location']['name']  #rename address as area
        (location,country) = location.split(',')
        #date_of_birth = extra_data['date-of-birth']  
        userProfile.location = location
        userProfile.country = country'''
        userProfile = MenteeProfile(user=user)
        userProfile.save()
        user.save()

        socialProfile = SocialProfiles.objects.get(parent=userProfile)
        socialProfile.profile_url_facebook = extra_data['link']
        socialProfile.profile_pic_url_facebook = "http://graph.facebook.com/"+extra_data['id']+"/picture"


        socialProfile.save()