from django.contrib import admin
from apps.mentee.models import MenteeProfile,SocialProfiles

class SocialInline(admin.TabularInline):
	model = SocialProfiles
	extra = 3

class MenteeProfileAdmin(admin.ModelAdmin):
	search_fields = ['location']
	list_filter = ['location']
	inlines = [SocialInline]

admin.site.register(MenteeProfile,MenteeProfileAdmin)
admin.site.register(SocialProfiles)

