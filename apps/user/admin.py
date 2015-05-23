from apps.mentee.models import Credits
from django.contrib import admin
from apps.user.models import Request, CallLog, Feedback, VerificationCodes, Notification


class RequestInline(admin.TabularInline):
    model = Request
    extra = 3

class CallLogInline(admin.TabularInline):
    model = CallLog
    extra = 3



class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Request)

admin.site.register(CallLog)

admin.site.register(Feedback)

admin.site.register(VerificationCodes)

admin.site.register(Notification)

admin.site.register(Credits)