from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

#import django User model
from django.contrib.auth.models import User

#import user profile models
from apps.user.models import UserProfile, SocialProfiles

#import specific forms
from apps.user.forms import UserForm,UserEditForm
from apps.mentee.forms import UserProfileForm
from random import choice
from string import letters
from allauth.socialaccount.models import SocialAccount,SocialApp

from PIL import Image
import os
def cropAndSave(user, POST):
    x1=POST['x1']
    x2=POST['x2']
    y1=POST['y1']
    y2=POST['y2']
    w=POST['w']
    h=POST['h']
    try:
        path = POST['url']
        im = Image.open(path)
        box = (x1, y1, x2, y2) #(left, upper, right, lower)
        box = (int(x) for x in box)
        cropped = im.crop(box)

        newPath = os.path.join(settings.MEDIA_ROOT,"profile_images",user.username)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        cropped.save(os.path.join(newPath,user.username+"CRPD.jpg"),"jpeg")
        im.save(os.path.join(newPath,user.username+".jpg"),"jpeg")
    except Exception as e:
        print str(e)

# Create your views here.
def index(request):
    context_dict = {}
    template = "user/loginV3.html" #default template to render
    user = None
    user_profile = None

    user = request.user.id
    if user != None:
        user_profile,created = UserProfile.objects.get_or_create(user=user)
    
    #Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/select.html" #User has to select either Mentor/Mentee,so redirect to select.html
        #attach required forms to display in the template

    if user_profile and not user_profile.is_new:

        template = "mentee/index.html"

    return render_to_response(template,context_dict,context_instance = RequestContext(request))

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

        data = request.POST.copy() # so we can manipulate data
        # random username
        data['username'] = data['email'] #useless,rather keep email as data['email'] username ''.join([choice(letters) for i in xrange(30)])
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
            {'user_form': user_form, 'profile_form': profile_form,'registered': registered},
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
    user_profile_object = user.user_profile
    social_profiles_object = None
    try:
        social_profiles_object = SocialProfiles.objects.get(parent=user_profile_object)
    except:
        pass
    # TODO add personal details after the user model
    # is finalized
    
    # initialize all to None
    context_dict['first_name'] = None
    context_dict['last_name'] = None
    context_dict['gender'] = None
    context_dict['date_of_birth'] = None
    context_dict['college'] = None
    context_dict['state'] = None
    context_dict['location'] = None 
    context_dict['country'] = None 
    context_dict['email'] = None 
    context_dict['contact_number'] = None
    context_dict['picture_url'] = None
    context_dict['profile_url'] = None

    gender_options={'male':"M",'female':'F'}

    first_name = user.first_name
    context_dict['first_name'] = first_name


    last_name = user.last_name
    context_dict['last_name'] = last_name

    gender = user_profile_object.gender
    if gender in gender_options.keys():
        context_dict['gender'] = gender_options[gender]

    date_of_birth = user_profile_object.date_of_birth
    if date_of_birth != '':
        context_dict['date_of_birth'] = date_of_birth

    location = user_profile_object.location
    if location != '':
        context_dict['location'] = location 
    
    country = user_profile_object.country
    if country != '':
        context_dict['country'] = country
    
    email_field = user.email
    if email_field != None:
        context_dict['email'] = email_field
    
    contact_number_field = user_profile_object.contact
    if contact_number_field != None:
        context_dict['contact_number'] = contact_number_field
    
    provider = None
    
    picture_url= None
    
    profile_url =None

    if social_profiles_object:
        if social_profiles_object.profile_pic_url_linkedin:
            provider = "LinkedIn"
            picture_url = social_profiles_object.profile_pic_url_linkedin
            profile_url = social_profiles_object.profile_url_linkedin
        elif social_profiles_object.profile_pic_url_facebook:
            provider = "Facebook"
            picture_url = social_profiles_object.profile_pic_url_facebook
            profile_url = social_profiles_object.profile_url_facebook

        if provider:
            context_dict['provider'] = provider

        if picture_url:
            context_dict['picture_url'] = picture_url 

        if profile_url:
            context_dict['profile_url'] = profile_url 
    
    return render_to_response("mentee/profile-view.html",context_dict,context)


@login_required
def edit_profile(request):
    # The following form method use taken from slide 66 of
    # http://www.slideshare.net/pydanny/advanced-django-forms-usage
    user = request.user
    user_profile = user.user_profile

    if request.POST:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid():
            user_profile = user_form.save()
            user_profile.save()
            if profile_form.is_valid():
                profile = profile_form.save()
                profile.save()
            # return here if different behaviour desired
    else:
        user_form = UserEditForm(instance=user)
        form = UserProfileForm(instance=user_profile)
    return render(request, "mentee/edit_profile.html", locals())


@login_required
def get_data(request,provider):
    return 

@login_required
def manage_social_profiles(request,action=None,provider=None):
    user = request.user
    #to get an actual live object from SimpleLazyObject
    user = User.objects.get(id=user.id)
    user_profile = UserProfile.objects.get(user=user)
    social_objects = SocialAccount.objects.filter(user=user)
    # dictionary stores all profile(profile-links/avatar-links) linked to different social apps
    if action == 'remove':
        try:
            if SocialAccount.objects.get(user=user,provider=provider):
                SocialAccount.objects.get(user=user,provider=provider).delete()
                sp = SocialProfiles.objects.get(parent=user_profile)
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
    sp_dict = {}
    for obj in social_objects:
        sp_dict[obj.provider] = {'profile_url':obj.get_profile_url(),'avatar_url':obj.get_avatar_url()}
    
    return render(request,'mentee/manage-social-profiles.html',locals())