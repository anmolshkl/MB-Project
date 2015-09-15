from apps.mentee.models import Credits
from django.contrib import admin
from apps.user.models import UserProfile, SocialProfile
from apps.mentor.models import EducationDetails, EmploymentDetails, UserActivity, Timings, Ratings
from django.contrib.auth.models import User


class SocialInline(admin.TabularInline):
    model = SocialProfile
    extra = 3


class EducationInline(admin.TabularInline):
    model = EducationDetails
    extra = 3


class EmploymentInline(admin.TabularInline):
    model = EmploymentDetails
    extra = 3


class UserActivityInline(admin.TabularInline):
    model = UserActivity
    extra = 3



class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['city']
    list_filter = ['city']
    inlines = [EducationInline, SocialInline, EmploymentInline]



admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(EducationDetails)
admin.site.register(SocialProfile)
admin.site.register(EmploymentDetails)
admin.site.register(UserActivity)
admin.site.register(Timings)
admin.site.register(Ratings)