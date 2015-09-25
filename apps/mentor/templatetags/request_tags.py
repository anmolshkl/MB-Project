from datetime import datetime
from apps.mentor.models import EducationDetails, Business_categories, Business_subcategories
from apps.user.models import Request, Notification
from django import template
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
import pytz

register = template.Library()


@register.simple_tag
def request_number(mentor_id):
    return Request.objects.filter(mentorId_id=mentor_id, is_approved=None, dateTime__gt=datetime.utcnow().replace(tzinfo=pytz.utc)
).count()


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
    notifications = Notification.objects.filter(to=int(id))
    count = notifications.count()
    notifications.count = count
    return notifications

@register.filter
@stringfilter
def filter_resume_name(name, arg):
    print arg
    name = str(arg).split("/").pop()
    return name

@register.assignment_tag
def get_categories():
    categories = Business_categories.objects.all()
    subcat_list = {}
    for cat in categories:
        subcategories = Business_subcategories.objects.filter(category=cat)
        subcat_list[cat] = subcategories

    return subcat_list
