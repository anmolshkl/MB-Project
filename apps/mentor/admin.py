from django.contrib import admin
from apps.mentor.models import UserProfile, EducationDetails, SocialProfiles

# Register your models here.
class EducationInline(admin.TabularInline):
	model = EducationDetails
	extra = 3
class UserProfileAdmin(admin.ModelAdmin):
	inlines = [EducationInline]

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(EducationDetails)
admin.site.register(SocialProfiles)
