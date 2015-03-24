from django.contrib import admin
from apps.user.models import UserProfile, SocialProfiles
from apps.mentor.models import EducationDetails, EmploymentDetails


class SocialInline(admin.TabularInline):
    model = SocialProfiles
    extra = 3


class EducationInline(admin.TabularInline):
    model = EducationDetails
    extra = 3


class EmploymentInline(admin.TabularInline):
    model = EmploymentDetails
    extra = 3


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['city']
    list_filter = ['city']
    inlines = [EducationInline, SocialInline, EmploymentInline]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EducationDetails)
admin.site.register(SocialProfiles)
admin.site.register(EmploymentDetails)
