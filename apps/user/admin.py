from django.contrib import admin
from apps.user.models import Request


class RequestInline(admin.TabularInline):
    model = Request
    extra = 3


class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Request)