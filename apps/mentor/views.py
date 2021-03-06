from time import strptime
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from apps.user.forms import UserForm, UserEditForm
from apps.mentor.forms import UserProfileForm, EducationForm, EmploymentForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.user.models import UserProfile, SocialProfile, Todo, Notification
from django.contrib.auth.models import User
from random import choice
from string import letters
from apps.mentor.forms import EducationDetailsFormSet, EmploymentDetailsFormSet
from apps.mentor.models import *
from allauth.socialaccount.models import SocialAccount, SocialApp
# Create your views here.
from django.conf import settings

from PIL import Image
from django.utils.html import strip_tags

import os

from django.http import JsonResponse

from apps.user.models import Request
from apps.mentor.models import UserActivity

from datetime import datetime as dt, timedelta as td, datetime, timedelta
from pytz import timezone
import pytz


def cropAndSave(user, POST):
    x1 = POST['x1']
    x2 = POST['x2']
    y1 = POST['y1']
    y2 = POST['y2']
    w = POST['w']
    h = POST['h']
    try:
        path = POST['url']
        im = Image.open(path)
        box = (x1, y1, x2, y2)  # (left, upper, right, lower)
        box = (int(x) for x in box)
        cropped = im.crop(box)
        newPath = os.path.join(settings.MEDIA_ROOT, "profile_images", user.username)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        cropped.save(os.path.join(newPath, user.username + "CRPD.jpg"), "jpeg")
        im.save(os.path.join(newPath, user.username + ".jpg"), "jpeg")
    except Exception as e:
        print str(e)
    return os.path.join(newPath, user.username + "CRPD.jpg")


def index(request):
    context_dict = {}
    template = "user/loginV3.html"  # default template to render
    user = None
    user_profile = None

    user = request.user.id
    if user != None:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
    else:
        return HttpResponseRedirect(settings.SITE_URL)

    # Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/selectV2.html"  # User has to select either Mentor/Mentee,so redirect to select.html
    if user_profile and not user_profile.is_new:
        if 'pic_url' in request.session:
            context_dict['pic_url'] = request.session['pic_url']
        try:
            todoList = Todo.objects.filter(parent=user)
            context_dict['todoList'] = todoList

        except ObjectDoesNotExist:
            pass
        try:
            timings = Timings.objects.get(parent=user)
            context_dict['timings'] = timings
        except ObjectDoesNotExist:
            pass
        template = "mentor/index.html"

    if user_profile.is_mentor is True and user_profile.is_bmentor is False:
        context_dict['completion_msg'] = '<a href="/mentor/edit-profile">Complete your profile</a>' \
                                         ' and provide us your past education details so that we can ' \
                                         'help mentee connect with you better.'
    elif user_profile.is_mentor is True and user_profile.is_bmentor is True:
        context_dict['completion_msg'] = '<a href="/mentor/edit-profile">Complete your profile</a>' \
                                         ' and provide your company/employment details so that we can ' \
                                         'help mentee connect with you better. You can also add your skills' \
                                         ', update information about yourself.'
    else:
        context_dict['completion_msg'] = '<a href="/mentor/edit-profile">Complete your profile</a>' \
                                         ' and update your information.'

    return render_to_response(template, context_dict, context_instance=RequestContext(request))


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        data = request.POST.copy()  # so we can manipulate data
        # random username
        data['username'] = data[
            'email']  # useless,rather keep email as data['email'] username ''.join([choice(letters) for i in xrange(30)])
        data['is_new'] = False
        user_form = UserForm(data)
        profile_form = UserProfileForm(data=request.POST)
        education_form = EducationForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid() and education_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.save()
            '''
            we dont need it now
            #now delete the default mentee profile thats created
            UserProfile.objects.get(user=user).delete()
            '''
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            cropAndSave(user, request.POST)
            if "url" in request.POST:
                profile.picture = request.POST['url']
            else:
                HttpResponse("Image URL missing :(")
            profile.is_new = False
            profile.is_mentor = True
            education = education_form.save(commit=False)
            education.parent = profile
            # employee = employment_form.save(commit=False)
            # employee.parent = profile

            profile.save()
            if education.institution != '':
                education.save()
                # if employee.organization != '':
                # employee.save()
            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect("/user/thank-you/")
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors, education_form.errors
            return HttpResponse("Invalid user Input.")

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        education_form = EducationForm()
        # employment_form = EmploymentForm()
    # Render the template depending on the context.
    return render_to_response(
        'mentor/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'education_form': education_form,
         'registered': registered},
        context)


@login_required
def self_profile_view(request):
    """
    This function returns all the fields 
    for viewing self profile
    """
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    user_profile_object = UserProfile.objects.get(user=user)
    if user_profile_object.is_new:
        return HttpResponseRedirect('/user/')

    # Social Profile
    try:
        social_profiles_object = SocialProfile.objects.get(parent=user_profile_object)
    except SocialProfile.DoesNotExist:
        social_profiles_object = None

    # Education Profile
    try:
        eduObjs = EducationDetails.objects.filter(parent=user_profile_object)
    except EducationDetails.DoesNotExist:
        eduObjs = None

    # Employment Profile
    try:
        empObjs = EmploymentDetails.objects.filter(parent=user_profile_object)
    except EmploymentDetails.DoesNotExist:
        empObjs = None

    try:
        timingsObj = Timings.objects.get(parent=user)
    except:
        timingsObj = None
    # TODO add personal details after the user model
    # is finalized
    # initialize all to None
    context_dict['full_name'] = None
    context_dict['gender'] = None
    context_dict['date_of_birth'] = None
    context_dict['city'] = None
    context_dict['country'] = None
    context_dict['college'] = None
    context_dict['email'] = None
    context_dict['contact_number'] = None
    context_dict['about'] = None
    context_dict['provider'] = None
    context_dict['picture_url'] = None
    context_dict['profile_url'] = None
    context_dict['edu_list'] = None
    context_dict['emp_list'] = None

    gender_options = {'male': "M", 'female': 'F'}

    name = user.first_name + " " + user.last_name
    context_dict['full_name'] = name

    gender = user_profile_object.gender
    if gender in gender_options.keys():
        context_dict['gender'] = gender_options[gender]

    date_of_birth = user_profile_object.date_of_birth
    if date_of_birth != '':
        context_dict['date_of_birth'] = date_of_birth

    city = user_profile_object.city
    if city != '':
        context_dict['city'] = city

    country = user_profile_object.country
    if country != '':
        context_dict['country'] = country

    email_field = user.email
    if email_field != None:
        context_dict['email'] = email_field

    contact = user_profile_object.contact
    if contact != None:
        context_dict['contact_number'] = contact

    about = user_profile_object.about
    if about:
        context_dict['about'] = about

    college = user_profile_object.college
    if college:
        context_dict['college'] = college

    picture_url = user_profile_object.picture
    if picture_url:
        context_dict['picture_url'] = picture_url

    provider = None

    profile_url = None

    if social_profiles_object:

        if social_profiles_object.profile_pic_url_linkedin:
            provider = "LinkedIn"
            picture_url = social_profiles_object.profile_pic_url_linkedin
            profile_url = social_profiles_object.profile_url_linkedin

            # If there is no pic uploaded, render LinkedIn pic
            if (not user_profile_object.picture):
                context_dict['pic_url'] = picture_url

        elif social_profiles_object.profile_pic_url_facebook:
            provider = "Facebook"
            picture_url = social_profiles_object.profile_pic_url_facebook
            profile_url = social_profiles_object.profile_url_facebook

        if provider:
            context_dict['provider'] = provider

        if context_dict['picture_url'] is None:
            context_dict['picture_url'] = picture_url

        if profile_url != None:
            context_dict['profile_url'] = profile_url
    if eduObjs:
        edu_list = []
        for obj in eduObjs:
            edu_list.append({'inst': obj.institution, 'city': obj.city, 'state': obj.state, 'country': obj.country,
                             'degree': obj.degree,
                             'branch': obj.branch, 'from': obj.from_year, 'to': obj.to_year, 'coun': obj.country})

        context_dict['edu_list'] = edu_list

    if empObjs:
        emp_list = []
        for obj in empObjs:
            emp_list.append({'org': obj.organization, 'loc': obj.location, 'pos': obj.position,
                             'from': obj.from_year, 'to': obj.to_year})

        context_dict['emp_list'] = emp_list

    context_dict['mentee_count'] = Request.objects.filter(mentorId=user.id, is_completed=True).count()
    rating_obj = {}
    try:
        rating_obj = Ratings.objects.get(mentor=user)
        average = int(round(rating_obj.average))
        rating_obj.activeStars = 'x' * average
        rating_obj.inactiveStars = 'x' * (5 - average)

    except ObjectDoesNotExist:
        rating_obj['count'] = 0
        rating_obj['one'] = 0
        rating_obj['two'] = 0
        rating_obj['three'] = 0
        rating_obj['four'] = 0
        rating_obj['five'] = 0
        rating_obj['average'] = 0

    context_dict['ratings'] = rating_obj

    context_dict['ratings'] = rating_obj

    # Specify timings too
    if timingsObj is not None:
        context_dict['weekday_l'] = timingsObj.weekday_l
        context_dict['weekday_u'] = timingsObj.weekday_u
        context_dict['weekend_l'] = timingsObj.weekend_l
        context_dict['weekend_u'] = timingsObj.weekend_u

    return render_to_response("mentor/profile-view.html", context_dict, context)


@login_required
def get_profile(request, mentorid):
    """
    This function returns all the fields
    for viewing mentor's profile
    """
    print "reached inside"
    context = RequestContext(request)
    context_dict = {}
    print mentorid
    userList = User.objects.all()
    for u in userList:
        print u.id
    try:
        user = User.objects.get(id=mentorid)

    except ObjectDoesNotExist:
        context_dict['error'] = "User doest not exist"
        return render_to_response("mentee/mentor-profile-view.html", context_dict, context)

    user_profile_object = UserProfile.objects.get(user=user)


    # Social Profile
    try:
        social_profiles_object = SocialProfile.objects.get(parent=user_profile_object)
    except SocialProfile.DoesNotExist:
        social_profiles_object = None

    # Education Profile
    try:
        eduObjs = EducationDetails.objects.filter(parent=user_profile_object)
    except EducationDetails.DoesNotExist:
        eduObjs = None

    # Employment Profile
    try:
        empObjs = EmploymentDetails.objects.filter(parent=user_profile_object)
    except EmploymentDetails.DoesNotExist:
        empObjs = None

    # Mentor timings
    try:
        timings_obj = Timings.objects.get(parent=user)
    except ObjectDoesNotExist:
        timings_obj = None

    print "still here"
    # TODO add personal details after the user model
    # is finalized
    # initialize all to None
    context_dict['full_name'] = None
    context_dict['gender'] = None
    context_dict['mentor_id'] = None
    context_dict['date_of_birth'] = None
    context_dict['city'] = None
    context_dict['country'] = None
    context_dict['college'] = None
    context_dict['email'] = None
    context_dict['contact_number'] = None
    context_dict['about'] = None
    context_dict['provider'] = None
    context_dict['picture_url'] = None
    context_dict['profile_url'] = None
    context_dict['edu_list'] = None
    context_dict['emp_list'] = None

    gender_options = {'male': "M", 'female': 'F'}

    name = user.first_name + " " + user.last_name
    print "hola"
    context_dict['full_name'] = name

    context_dict['mentor_id'] = mentorid

    gender = user_profile_object.gender
    if gender in gender_options.keys():
        context_dict['gender'] = gender_options[gender]

    date_of_birth = user_profile_object.date_of_birth
    if date_of_birth != '':
        context_dict['date_of_birth'] = date_of_birth

    city = user_profile_object.city
    if city != '':
        context_dict['city'] = city

    country = user_profile_object.country
    if country != '':
        context_dict['country'] = country

    email_field = user.email
    if email_field != None:
        context_dict['email'] = email_field

    contact = user_profile_object.contact
    if contact != None:
        context_dict['contact_number'] = contact

    about = user_profile_object.about
    if about:
        context_dict['about'] = about

    college = user_profile_object.college
    if college:
        context_dict['college'] = college

    picture_url = user_profile_object.picture
    if picture_url:
        context_dict['picture_url'] = picture_url

    '''
    NO NEED FOR SOCIAL DETAILS
    if social_profiles_object:

        if social_profiles_object.profile_pic_url_linkedin:
            provider = "LinkedIn"
            picture_url = social_profiles_object.profile_pic_url_linkedin
            profile_url = social_profiles_object.profile_url_linkedin

            # If there is no pic uploaded, render LinkedIn pic
            if not user_profile_object.picture:
                context_dict['picture_url'] = picture_url

        elif social_profiles_object.profile_pic_url_facebook:
            provider = "Facebook"
            picture_url = social_profiles_object.profile_pic_url_facebook
            profile_url = social_profiles_object.profile_url_facebook

        if provider:
            context_dict['provider'] = provider

        if picture_url != None:
            context_dict['picture_url'] = picture_url

        if profile_url != None:
            context_dict['profile_url'] = profile_url
    '''

    if eduObjs:
        edu_list = []
        for obj in eduObjs:
            edu_list.append({'inst': obj.institution, 'loc': obj.location, 'degree': obj.degree,
                             'branch': obj.branch, 'from': obj.from_year, 'to': obj.to_year, 'country': obj.country})

        context_dict['edu_list'] = edu_list

    if empObjs:
        emp_list = []
        for obj in empObjs:
            emp_list.append({'org': obj.organization, 'loc': obj.location, 'pos': obj.position,
                             'from': obj.from_year, 'to': obj.to_year})

        context_dict['emp_list'] = emp_list

    if timings_obj:
        context_dict['weekday_l'] = timings_obj.weekday_l
        context_dict['weekday_u'] = timings_obj.weekday_u
        context_dict['weekend_l'] = timings_obj.weekend_l
        context_dict['weekend_u'] = timings_obj.weekend_u

    context_dict['timezone'] = user_profile_object.timezone

    rating_obj = {}
    try:
        rating_obj = Ratings.objects.get(mentor=user)
        average = int(round(rating_obj.average))
        rating_obj.activeStars = 'x' * average
        rating_obj.inactiveStars = 'x' * (5 - average)

    except ObjectDoesNotExist:
        rating_obj['count'] = 0
        rating_obj['one'] = 0
        rating_obj['two'] = 0
        rating_obj['three'] = 0
        rating_obj['four'] = 0
        rating_obj['five'] = 0
        rating_obj['average'] = 0

    context_dict['ratings'] = rating_obj

    return render_to_response("mentee/mentor-profile-view.html", context_dict, context)


@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.user_profile

    if request.method == 'POST' and request.POST:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        edu_formset = EducationDetailsFormSet(request.POST, instance=user_profile)
        emp_formset = EmploymentDetailsFormSet(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid() and edu_formset.is_valid() and emp_formset.is_valid():
            if "url" in request.POST:
                user_profile.picture = cropAndSave(user, request.POST)
                user_profile.save()

            user_form.save()
            profile_form.save()
            emp_formset.save()
            edu_formset.save()
            return render(request, "mentor/edit_profile.html", locals())
            # return here if different behaviour desired
        else:
            print user_form.errors
            print profile_form.errors
            return render(request, "mentor/edit_profile.html", locals())
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
        edu_formset = EducationDetailsFormSet(instance=user_profile)
        emp_formset = EmploymentDetailsFormSet(instance=user_profile)

    context = RequestContext(request)
    context_dict = {}

    categories = Business_categories.objects.all()

    dict_index = 0;
    for cat in categories:
        subcat_list = []
        subcategories = Business_subcategories.objects.filter(category_id=cat.id)
        subcat_list.append({'category_id': cat.id, 'category_name': cat.name, 'subcategories': subcategories})
        context_dict[dict_index] = subcat_list
        dict_index = dict_index + 1

    tags = Business_Mentor_Tags.objects.filter(mentor=user_profile)

    return render(request, "mentor/edit_profile.html", locals())


@login_required
def get_data(request):
    user = request.user
    user = User.objects.get(id=user.id)
    extra_data = None
    try:
        extra_data = user.socialaccount_set.filter(provider='linkedin')[0].extra_data
    except:
        pass
    if extra_data:
        location = extra_data['location']['name']  # rename address as area
        first_name = extra_data['first-name']
        last_name = extra_data['last-name']
        user.first_name = first_name
        user.last_name = last_name
        (location, country) = location.split(',')
        # date_of_birth = extra_data['date-of-birth']
        userProfile = UserProfile.objects.get(user=user)
        userProfile.location = location
        userProfile.country = country
        userProfile.save()
        user.save()

        # Save Education Data if received
        if 'educations' in extra_data:
            educations = extra_data['educations']['education']

        if educations:
            for individual_edu in educations:
                if not EducationDetails.objects.filter(parent=user, institution=individual_edu['school-name']):
                    edu_profile = EducationDetails.objects.create(parent=userProfile)
                    edu_profile.institution = individual_edu['school-name']
                    edu_profile.location = ""
                    if 'field-of-study' in individual_edu:
                        edu_profile.branch = individual_edu['field-of-study']
                    if 'degree' in individual_edu:
                        edu_profile.degree = individual_edu['degree']
                    edu_profile.from_year = individual_edu['start-date']['year']
                    edu_profile.to_year = individual_edu['end-date']['year']
                    edu_profile.country = ""
                    edu_profile.save()
        socialProfile, created = SocialProfile.objects.get_or_create(parent=userProfile)
        # socialProfile = SocialProfiles(parent=userProfile)
        socialProfile.profile_url_linkedin = extra_data['public-profile-url']
        socialProfile.profile_pic_url_linkedin = extra_data['picture-url']
        socialProfile.save()
    return HttpResponseRedirect("/mentor/edit-profile/")


@login_required
def manage_social_profiles(request, action=None, provider=None):
    user = request.user
    context_dict = {}
    # to get an actual live object from SimpleLazyObject
    user = User.objects.get(id=user.id)
    user_profile = UserProfile.objects.get(user=user)
    if action == 'remove':
        try:
            sp = SocialProfile.objects.get(parent=user_profile)
            if provider == 'facebook':
                sp.profile_pic_url_facebook = ""
                sp.profile_url_facebook = ""
            if provider == 'linkedin':
                sp.profile_pic_url_linkedin = ""
                sp.profile_url_linkedin = ""
            if provider == 'google':
                sp.profile_pic_url_google = ""
                sp.profile_url_google = ""
            if provider == 'github':
                sp.profile_pic_url_github = ''
                sp.profile_url_github = ''
            sp.save()
        except SocialAccount.DoesNotExist:
            pass
    try:
        social_profile = user_profile.social_profiles
    except ObjectDoesNotExist:
        social_profile = None
    context_dict['sp'] = social_profile
    return render(request, 'mentor/manage-social-profiles.html', context_dict, context_instance=RequestContext(request))


@login_required
def getCalendar(request):
    return render_to_response()


@login_required
def live(request):
    return render_to_response('mentor/live.html', {}, RequestContext(request))


# A Utility function to - whether the Mentor is available on a given date and time
def check_mentor_availibility(request, date, time, max_duration, mentor_id):
    response = True
    # Convert date & time in django friendly format
    date_time = dt.strptime(date + " " + time, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
    date_time = dt.strptime(date_time, '%Y-%m-%d %H:%M')

    tz = timezone(request.user.user_profile.timezone)
    d_tz = tz.normalize(tz.localize(date_time))
    d_utc = d_tz.astimezone(pytz.utc)

    requests = Request.objects.filter(mentorId_id=mentor_id,
                                      dateTime__gte=d_utc - td(minutes=max_duration / 2),
                                      dateTime__lte=d_utc + td(minutes=max_duration / 2))
    if requests:
        response = False
    return response


# A Utility function to check whether the Mentee is available on a given date and time
def check_mentee_availibility(request, date, time, max_duration, mentee_id):
    response = True

    # Convert date & time in django friendly format
    date_time = dt.strptime(date + " " + time, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
    date_time = dt.strptime(date_time, '%Y-%m-%d %H:%M')

    tz = timezone(request.user.user_profile.timezone)
    d_tz = tz.normalize(tz.localize(date_time))
    d_utc = d_tz.astimezone(pytz.utc)
    requests = Request.objects.filter(menteeId_id=mentee_id,
                                      dateTime__gte=d_utc - td(minutes=max_duration / 2),
                                      dateTime__lte=d_utc + td(minutes=max_duration / 2))
    if requests:
        response = False

    return response


def check_mentee_balance(mentee_id, duration, call_type):
    available = True
    credits_obj = User.objects.get(id=int(mentee_id)).credits
    print credits_obj.balance
    if call_type == "1":
        # Web to Web
        if duration * 3 > credits_obj.balance:
            available = False
            print duration * 3
    elif call_type == "2":
        # Web to phone
        if duration * 6 > credits_obj.balance:
            available = False
    elif call_type == "3":
        # Video
        if duration * 5 > credits_obj.balance:
            available = False

    print "balance={0}".format(available)
    return available


@login_required
def check_availability(request):
    date1 = request.POST['date1']
    time1 = request.POST['time1']
    dur1 = int(request.POST['dur1'])
    date2 = request.POST['date2']
    time2 = request.POST['time2']
    dur2 = int(request.POST['dur2'])
    mentor_id = request.POST['mentor_id']
    mentee_id = request.POST['mentee_id']
    call_type = request.POST['call_type']
    response = {
        '1': check_mentor_availibility(request, date1, time1, 30, mentor_id) and check_mentee_availibility(request,
                                                                                                           date1, time1,
                                                                                                           30,
                                                                                                           mentee_id) and check_mentee_balance(
            mentee_id, dur1, call_type),
        '2': check_mentor_availibility(request, date2, time2, 30, mentor_id) and check_mentee_availibility(request,
                                                                                                           date2, time2,
                                                                                                           30,
                                                                                                           mentee_id) and check_mentee_balance(
            mentee_id, dur2, call_type)}
    return JsonResponse(response)


@login_required
def send_request(request):
    # extract the POST dictionary
    post = request.POST
    error = False
    msg = None
    if 'date' in post and 'time' in post and 'duration' in post and 'mentor_id' in post and 'callType' in post:
        if post['date'] != '' and post['time'] != '' and post['duration'] != '' and post['mentor_id'] != '' \
                and 4 > int(post['callType']) > 0:
            if 5 <= int(post['duration']) <= 30:
                if check_mentor_availibility(request, post['date'], post['time'], 30, post['mentor_id']) \
                        and check_mentee_availibility(request, post['date'], post['time'], 30, int(post['mentee_id'])) \
                        and check_mentee_balance(post['mentee_id'], int(post['duration']), int(post['call_type'])):
                    date_time = dt.strptime(post['date'] + " " + post['time'], '%d/%m/%Y %H:%M').strftime(
                        '%Y-%m-%d %H:%M')
                    date_time = dt.strptime(date_time, '%Y-%m-%d %H:%M')
                    tz = timezone(request.user.user_profile.timezone)
                    d_tz = tz.normalize(tz.localize(date_time))
                    d_utc = d_tz.astimezone(pytz.utc)
                    print tz
                    print "request time in UTC={0}".format(d_utc)
                    request_obj = Request(menteeId_id=request.user.id, mentorId_id=post['mentor_id'],
                                          dateTime=d_utc, duration=post['duration'],
                                          callType=post['callType'], message=post['message'])
                    request_obj.save()

                    # Send notification email to MENTOR
                    mentor_name = request_obj.mentorId.get_full_name()
                    mentor_email = request_obj.mentorId.email
                    print mentor_name
                    print mentor_email
                    email_subject = 'New request from {0}'.format(request.user.get_full_name())
                    email_body = "Hello Mentor,<br><br>You have a new request from {0}, kindly respond to it " \
                                 "within 48 hours.<br><br>Regards,<br>MB Team".format(mentor_name)
                    text_content = strip_tags(email_body)  # this strips the html, so people will have the text as well.
                    email = EmailMultiAlternatives(email_subject, text_content, 'buddy@mentorbuddy.in',
                                                 [mentor_email])
                    email.attach_alternative(email_body, "text/html")
                    email.send()
                    msg = "Request has been successfully sent! We'll notify you once the mentor responds to it."
                else:
                    error = True
                    msg = 'Sorry! The mentor is unavailable during this time.<br>Please select another time & date.'
            else:
                error = True
                msg = "Duration has to between 5-30 min."
        else:
            error = True
            msg = 'Received Empty Fields. Try Again!'
    else:
        error = True
        msg = 'Missing Fields. Try Again!'

    json_obj = {"error": error, "msg": msg}
    return JsonResponse(json_obj)


@login_required
def get_requests(request):
    user = request.user
    context = RequestContext(request)
    context_dict = {}
    req_objs = Request.objects.filter(mentorId=user.id, is_approved=None, dateTime__gte=datetime.now(pytz.utc))
    tz = pytz.UTC
    if req_objs:
        req_list = []
        for obj in req_objs:
            mentee = User.objects.get(id=obj.menteeId_id)
            d_tz = obj.dateTime.astimezone(timezone(request.user.user_profile.timezone))
            req_list.append({'request_id': obj.id, 'date': d_tz.date(), 'time': d_tz.time(),
                             'dateTime': obj.dateTime,
                             'duration': obj.duration,
                             'callType': obj.callType, 'req_date': obj.requestDate,
                             "mentee_name": mentee.get_full_name(),
                             "country": mentee.user_profile.country,
                             "message": obj.message})
            context_dict['req_list'] = req_list

    return render_to_response("mentor/requests.html", context_dict, context)


@login_required
def handle_request(request):
    error = False
    response = {}
    post = request.POST
    if "request_id" in post and "status" in post and post["request_id"] != '' and post['status'] != '':
        if post['status'] == '1':
            # approve the request
            req = Request.objects.get(id=post["request_id"])
            req.is_approved = True
            req.save()
            # create new notification
            notif_obj = Notification.objects.create(to=req.menteeId)
            notif_obj.frm = "admin"
            notif_obj.text = "Your request has been approved by {0}. Please put a reminder but we'll still remind you " \
                             ";)".format(request.user.get_full_name())
            notif_obj.title = "Request approved!"
            notif_obj.save()

            # Send notification email to mentee
            mentee_name = req.menteeId.get_full_name()
            mentee_email =req.menteeId.email
            email_subject = 'Request approved by {0}'.format(request.user.get_full_name())
            email_body = "Greetings Mentee!<br><br>Your requests has been approved by {0}, kindly make yourself " \
                         "available on {1} GMT. In case you forget, we'll still remind you 15 mins before the call :)" \
                         "<br><br>Regards,<br>MB Team".format(mentee_name, req.dateTime)
            text_content = strip_tags(email_body)  # this strips the html, so people will have the text as well.
            email = EmailMultiAlternatives(email_subject, text_content, 'buddy@mentorbuddy.in', [mentee_email])
            email.attach_alternative(email_body, "text/html")
            email.send()

        elif post['status'] == '0':
            # disapprove the request
            req = Request.objects.get(id=post["request_id"])
            req.is_approved = False
            req.save()
            notif_obj = Notification.objects.create(to=req.menteeId)
            notif_obj.frm = "admin"
            notif_obj.text = "Your request is not approved by {0}. Please select a different time/date/mentor".format(
                request.user.get_full_name())
            notif_obj.title = "Request disapproved!"
            notif_obj.save()
        else:
            error = True
    else:
        error = True
    return JsonResponse({"error":error})


@login_required
def get_calendar(request):
    user = request.user
    context = RequestContext(request)
    context_dict = {}
    req_objs = Request.objects.filter(mentorId=user.id)
    tz = pytz.utc
    if req_objs:
        req_list = []
        for obj in req_objs:
            mentee = User.objects.get(id=obj.menteeId_id)
            d_tz = obj.dateTime.astimezone(timezone(request.user.user_profile.timezone))
            end = d_tz + td(minutes=obj.duration)
            req_list.append({'request_id': obj.id, 'startDateTime': d_tz,
                             'endDateTime': end,
                             'duration': obj.duration,
                             'status': obj.is_approved,
                             'callType': obj.callType, 'req_date': obj.requestDate,
                             "mentee_name": mentee.get_full_name(), "country": mentee.user_profile.country})
            context_dict['req_list'] = req_list

    return render_to_response("mentor/calendar.html", context_dict, context)


@login_required
def update_last_seen(request):
    if request.GET['id'] and request.GET['id'] is not '':
        user = User.objects.get(id=int(request.GET['id']))
        try:
            activity = UserActivity.objects.get(mentor=user)
        except ObjectDoesNotExist:
            activity = UserActivity()
            activity.mentor = user
        activity.last_seen = datetime.now(pytz.utc)
        activity.save()
        return JsonResponse({'error': False})
    else:
        return JsonResponse({'error': True})


@login_required
def check_mentor_status(request):
    if 'id' in request.GET and request.GET['id'] != '':
        user = User.objects.get(id=int(request.GET['id']))
        try:
            activity = user.activity
        except ObjectDoesNotExist:
            activity = None
        status = "offline"
        error = False
        if activity != None and activity.last_seen >= datetime.now(pytz.utc) - timedelta(minutes=2):
            status = "online"
    else:
        error = True

    return JsonResponse({'error': error, 'status': status})


@login_required
def update_timings(request):
    timings = Timings(parent=request.user)
    post = request.POST
    error = False
    msg = None
    if request.method == 'POST':
        if 'weekday_l' in post and 'weekday_u' in post and 'weekend_l' in post and 'weekend_u' in post:
            try:
                timings.weekday_l = post['weekday_l']
                timings.weekday_u = post['weekday_u']
                timings.weekend_l = post['weekend_l']
                timings.weekend_u = post['weekend_l']
                timings.save()
            except ValueError:
                error = True
                msg = "Unsupported time format"
        else:
            error = True
            msg = "Missing time field/s"
    else:
        error = True
        msg = "Not a post request"

    return JsonResponse({'error': error, 'msg': msg})


@login_required
def update_tags(request):
    context = RequestContext(request)
    context_dict = {}

    categories = Business_categories.objects.all()

    dict_index = 0;
    for cat in categories:
        subcat_list = []
        print cat.name
        subcategories = Business_subcategories.objects.filter(category_id=cat.id)
        print subcategories
        subcat_list.append({'category_id': cat.id, 'category_name': cat.name, 'subcategories': subcategories})
        context_dict[dict_index] = subcat_list
        dict_index = dict_index + 1

    return render_to_response("mentor/update_tags.html",
                              {'categories': categories, 'context_dict': context_dict, 'context': context})


@login_required
def save_tags(request):
    user = request.user
    user_profile = user.user_profile
    user_id = user.id
    b_id = user_profile.is_bmentor

    post = request.POST

    if request.method == 'POST' and request.POST:
        if 'subcategory_id' in post:

            bmentor_profile = UserProfile.objects.get(user_id=user_id)
            bmentor_profile.is_bmentor = 1
            bmentor_profile.save()

            subcat = Business_subcategories.objects.get(id=post['subcategory_id'])

            try:
                mapping = Business_Mentor_Tags.objects.create(mentor=user_profile, subcategory=subcat)
            except Exception:
                return JsonResponse({'error': True, 'msg': 'Tag already exists'})
            mapping.save()
            return JsonResponse({'error': False, 'msg': 'Tag saved'})

    print "in savetags view"

    return HttpResponseRedirect("/mentor/")


@login_required
def get_tags(request):
    user = request.user
    user_profile = user.user_profile
    subcat_tag_list = Business_Mentor_Tags.objects.filter(mentor=user_profile)

    context = RequestContext(request)
    context_dict = {}

    dict_index = 0;
    for tag in subcat_tag_list:
        cat_subcat_list = []

        # subcat = Business_subcategories.objects.get(id=subcat_id)

        subcat_name = tag.subcategory.name

        cat_name = Business_subcategories.objects.get(id=tag.subcategory.id).category.name

        cat_subcat_list.append({'category': cat_name, 'subcategory': subcat_name})
        context_dict[dict_index] = cat_subcat_list
        dict_index = dict_index + 1

    print context_dict
    return HttpResponseRedirect("/mentor/")
