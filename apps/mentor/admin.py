from django.contrib import admin
from apps.mentor.models import UserProfile, EducationDetails, SocialProfiles

class SocialInline(admin.TabularInline):
	model = SocialProfiles
	extra = 3
class EducationInline(admin.TabularInline):
	model = EducationDetails
	extra = 3
class UserProfileAdmin(admin.ModelAdmin):
	search_fields = ['location']
	list_filter = ['location']
	inlines = [EducationInline,SocialInline]

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(EducationDetails)
admin.site.register(SocialProfiles)
