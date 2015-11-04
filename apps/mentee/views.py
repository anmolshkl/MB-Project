from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

# import django User model
from django.contrib.auth.models import User

#import user profile models
from apps.user.models import UserProfile, SocialProfile, Request, Todo

#import specific forms
from apps.user.forms import UserForm, UserEditForm
from apps.mentee.forms import UserProfileForm
from random import choice
from string import letters
from allauth.socialaccount.models import SocialAccount, SocialApp

from PIL import Image
from django.utils.datetime_safe import datetime
from mentorbuddy import settings
import os
import pytz


def cropAndSave(user, POST):
    print "entered crop and save"
    x1 = POST['x1']
    x2 = POST['x2']
    y1 = POST['y1']
    y2 = POST['y2']
    w = POST['w']
    h = POST['h']
    try:
        path = POST['url']
        im = Image.open(path)
        box = (x1, y1, x2, y2)  #(left, upper, right, lower)
        box = (int(x) for x in box)
        cropped = im.crop(box)
        print "2"
        newPath = os.path.join(settings.MEDIA_ROOT, "profile_images", str(user.id))
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        cropped.save(os.path.join(newPath, str(user.id) + "CRPD.jpg"), "jpeg")
        im.save(os.path.join(newPath, str(user.id) + ".jpg"), "jpeg")
    except Exception as e:
        print str(e)

    return os.path.join(newPath, str(user.id) + "CRPD.jpg")


# Create your views here.
def index(request):
    context_dict = {}
    template = "user/loginV3.html"  #default template to render
    user = None
    user_profile = None

    user = request.user.id
    if user != None:
        user_profile, created = UserProfile.objects.get_or_create(user=user)

    #Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/selectV2.html"  #User has to select either Mentor/Mentee,so redirect to select.html
        #attach required forms to display in the template

    if user_profile and not user_profile.is_new:
        todoList = Todo.objects.filter(parent=user)
        context_dict['todoList'] = todoList
        template = "mentee/index.html"

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
            'email']  #useless,rather keep email as data['email'] username ''.join([choice(letters) for i in xrange(30)])
        user_form = UserForm(data)
        profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            #MISTAKE-was rehashing the hashed password,user.set_password(user.password)
            user.save()

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
            profile.is_mentor = False
            profile.save()
            # Update our variable to tell the template registration was successful.
            registered = True
            return HttpResponseRedirect("/user/thank-you/")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render_to_response(
        'mentee/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
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

    gender_options = {'male': "M", 'female': 'F'}

    contact = user_profile_object.contact
    if contact is not None:
        context_dict['contact_number'] = contact

    about = user_profile_object.about
    if about is not None:
        context_dict['about'] = about

    college = user_profile_object.college
    if college is not None:
        context_dict['college'] = college
        print "college"

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

    provider = None

    picture_url = user_profile_object.picture  # set default profile image
    context_dict['picture_url'] = picture_url
    profile_url = None

    if social_profiles_object:

        if social_profiles_object.profile_pic_url_linkedin:
            provider = "LinkedIn"
            picture_url = social_profiles_object.profile_pic_url_linkedin
            profile_url = social_profiles_object.profile_url_linkedin

            # If there is no pic uploaded, render LinkedIn pic
            if picture_url is not None:
                context_dict['picture_url'] = picture_url

        elif social_profiles_object.profile_pic_url_facebook:
            provider = "Facebook"
            picture_url = social_profiles_object.profile_pic_url_facebook
            profile_url = social_profiles_object.profile_url_facebook

        if provider:
            context_dict['provider'] = provider

        if picture_url is not None:
            context_dict['picture_url'] = picture_url

        if profile_url is not None:
            context_dict['profile_url'] = profile_url

    context_dict['balance'] = user.credits.balance
    context_dict['mentor_count'] = Request.objects.filter(menteeId=user.id, is_completed=True).count()
    return render_to_response("mentee/profile-view.html", context_dict, context)


@login_required
def edit_profile(request):
    user = request.user
    user_profile = user.user_profile
    error = False
    msg = None

    if request.POST:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid():
            user_profile = user_form.save(commit=False)
            user_profile.save()
            profile_form.is_valid()
            print profile_form
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                if "url" in request.POST:
                    profile.picture = cropAndSave(user, request.POST)
                # return here if different behaviour desired
                profile.save()

                return JsonResponse({error: False,msg: "Profile Updated!"})
            else:
                return JsonResponse({error: True,msg: "Please check the required fields"})
        else:
            return JsonResponse({error: True,msg: "Please check the required fields"})
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, "mentee/edit_profile.html", locals())


@login_required
def get_data(request, provider):
    return


@login_required
def manage_social_profiles(request, action=None, provider=None):
    user = request.user
    context_dict = {}
    # to get an actual live object from SimpleLazyObject
    user = User.objects.get(id=user.id)
    user_profile = UserProfile.objects.get(user=user)
    try:
        social_profile = user_profile.social_profiles
    except ObjectDoesNotExist:
        social_profile = None
    context_dict['sp'] = social_profile
    return render(request, 'mentee/manage-social-profiles.html', context_dict, context_instance=RequestContext(request))


@login_required()
def requests(request):
    user = request.user
    contextDic = {}
    request_list = []
    u = datetime.utcnow()
    u = u.replace(tzinfo=pytz.user.)
    userRequests = Request.objects.filter(menteeId=user.id, dateTime__gte=u).order_by('dateTime')
    for reqObj in userRequests:
        obj = {}
        obj['mentorId'] = reqObj.mentorId
        obj['mentorName'] = User.objects.get(id=reqObj.mentorId_id).get_full_name()
        obj['picture'] = User.objects.get(id=reqObj.mentorId_id).user_profile.picture

        obj['dateTime'] = reqObj.dateTime.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(user.user_profile.timezone))
        obj["is_approved"] = reqObj.is_approved
        obj["callType"] = reqObj.callType
        obj["is_rescheduled"] = reqObj.is_rescheduled
        obj["duration"] = reqObj.duration
        obj["requestDate"] = reqObj.requestDate
        request_list.append(obj)
    contextDic['userRequests'] = request_list
    print request_list
    return render_to_response('mentee/requests.html', contextDic, RequestContext(request))
