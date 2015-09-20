from apps.mentee.models import Credits
from django.contrib import admin
from apps.user.models import UserProfile, SocialProfile
from apps.mentor.models import *
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



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def fullname(self,object):
        return object.user.get_full_name()

    fullname.admin_order_field = 'user'
    fullname.short_description = "Full Name"

    search_fields = ['city', 'country']
    list_filter = ['city', 'country', 'is_mentor']
    list_display = ('user', 'fullname', 'is_mentor')
    inlines = [EducationInline, SocialInline, EmploymentInline]


admin.site.register(EducationDetails)
admin.site.register(SocialProfile)
admin.site.register(EmploymentDetails)
admin.site.register(UserActivity)
admin.site.register(Timings)
admin.site.register(Ratings)
admin.site.register(Business_categories)
admin.site.register(Business_subcategories)
admin.site.register(Business_Mentor_Tags)
