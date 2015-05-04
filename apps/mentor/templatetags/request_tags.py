from apps.user.models import Request
from django import template

register = template.Library()

@register.simple_tag
def request_number(mentor_id):
    return Request.objects.filter(mentorId_id=mentor_id, is_approved=None).count()

