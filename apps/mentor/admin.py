from django.contrib import admin
from apps.mentor.models import MentorProfile, EducationDetails, SocialProfiles

class SocialInline(admin.TabularInline):
	model = SocialProfiles
	extra = 3
class EducationInline(admin.TabularInline):
	model = EducationDetails
	extra = 3
class MentorProfileAdmin(admin.ModelAdmin):
	search_fields = ['location']
	list_filter = ['location']
	inlines = [EducationInline,SocialInline]

admin.site.register(MentorProfile,MentorProfileAdmin)
admin.site.register(EducationDetails)
admin.site.register(SocialProfiles)
