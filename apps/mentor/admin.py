from django.contrib import admin
from apps.mentor.models import UserProfile, EducationDetails, SocialProfiles

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(EducationDetails)
admin.site.register(SocialProfiles)
