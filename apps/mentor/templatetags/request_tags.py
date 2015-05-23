from apps.mentor.models import EducationDetails
from apps.user.models import Request, Notification
from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def request_number(mentor_id):
    return Request.objects.filter(mentorId_id=mentor_id, is_approved=None).count()


@register.simple_tag
def profile_progress(mentor_id):
    user = User.objects.get(id=mentor_id)
    userProfile = user.user_profile
    eduProfile = EducationDetails.objects.filter(parent=userProfile)
    userProfileFields = userProfile.__dict__
    blank = 0
    total = len(userProfileFields.keys()) - 8
    for field, value in userProfileFields.items():
        if value == '' or value is None:
            blank += 1
    if eduProfile.count() == 1:
        eduProfileFields = eduProfile.__dict__
        total += len(eduProfileFields.keys()) - 3
        for field, value in eduProfileFields.items():
            if value == '' or value is None:
                blank += 1
    return (total - blank) * 100 / total


@register.assignment_tag
def get_notifications(id):
    return Notification.objects.filter(to=int(id))

