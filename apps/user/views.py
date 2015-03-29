from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import authenticate, login, logout  # ,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from apps.user.models import UserProfile, SocialProfiles, MentorSearchForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# new
#from apps.user.backends import EmailAuthBackend 
from django.conf import settings

from PIL import Image

#import magic
# Create your views here.
from django.core.mail import send_mail


def sendMail(request):
    send_mail('Its Working', 'Put your Email message here.', 'anmol@mentorbuddy.in', ['Anmol.shkl@gmail.com'],
              fail_silently=False)
    return HttpResponseRedirect('http://www.gmail.com')


import os


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
        box = (x1, y1, x2, y2)  #(left, upper, right, lower)
        box = (int(x) for x in box)
        cropped = im.crop(box)
        newPath = os.path.join(settings.MEDIA_ROOT, "profile_images", user.username)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        cropped.save(os.path.join(newPath, user.username + "CRPD.jpg"), "jpeg")
        im.save(os.path.join(newPath, user.username + ".jpg"), "jpeg")
    except Exception as e:
        print str(e)


def index(request):
    context_dict = {}
    template = "user/loginV3.html"  #default template to render
    user = None
    user_profile = None

    if request.user.is_authenticated():
        user_profile, created = UserProfile.objects.get_or_create(user=request.user.id)

    #Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/select.html"  #User has to select either Mentor/Mentee,so redirect to select.html
        #attach required forms to display in the template

    if user_profile and not user_profile.is_new:
        if user_profile.is_mentor == True:
            return HttpResponseRedirect("/mentor/")
        else:
            return HttpResponseRedirect("/mentee/")

    return render_to_response(template, context_dict, context_instance=RequestContext(request))


def user_login(request):
    # Like before, obtain the context for the user's request.
    print "inside user_login view"
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['loginEmail']
        password = request.POST['loginPassword']
        user = authenticate(username=email, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the userpage.
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                (social_profile, created) = SocialProfiles.objects.get_or_create(parent=user_profile)
                return HttpResponseRedirect("/user/")
                #return HttpResponseRedirect('/user/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponseRedirect("/user/")
                #return HttpResponse("Your Mentor Buddy account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            #return HttpResponse("Invalid login details supplied.")
            return render_to_response('user/loginV3.html', {'error': "Invalid Email/Password"},
                                      context_instance=context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GETself.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('user/loginV3.html', {}, context_instance=context)
    return render_to_response('user/loginV3.html', {}, context_instance=context)


def select(request):
    error = False
    msg = None
    template = "user/select.html"
    user = request.user
    user_profile = user.user_profile

    if not UserProfile.objects.get(user=request.user).is_new:
        return HttpResponseRedirect('/user/')

    if request.method == 'POST':
        #check whether a request is POST request after submitted choice has come
        if 'choice' in request.POST:
            if request.POST['choice'] == "mentor":
                user_profile.is_mentor = True
                user_profile.save()
            elif request.POST['choice'] == "mentee":
                user_profile.is_mentor = False
                user_profile.save()
            else:
                error = True
                msg = "Not a valid choice!"
        else:
            error = True
            msg = "Select an option!"

    return JsonResponse({"error": error, "message": msg})


def set_password(request):
    error = False
    msg = None
    template = "user/select.html"
    user = request.user
    user_profile = user.user_profile
    if not UserProfile.objects.get(user=request.user).is_new:
        return HttpResponseRedirect('/user/')

    if request.method == 'POST':
        #check whether a request is POST request after submitted choice has come
        if 'password' in request.POST and 'confirmPassword' in request.POST:
            if request.POST['password'] == request.POST['confirmPassword'] and request.POST['password'] != '':
                if len(request.POST['password']) >= 6:
                    user.set_password(request.POST['password'])
                    user.save()

                    #check if it's a new user
                    if user_profile.is_new:
                        user_profile.is_new = False
                        user_profile.save()
                else:
                    error = True
                    msg = "Password should be atleast 6 characters long."
            else:
                error = True
                msg = "Password empty or doesnt matches confirmation password."
        else:
            error = True
            msg = "Didn't receive password!"

    return JsonResponse({"error": error, "message": msg})


def register(request):
    post = request.POST  #for convenience
    msg = None
    #check if we got all the input fields
    if request.method == 'POST' and 'fn' in post and 'ln' in post and 'email' in post and 'college' in post and 'city' in post and 'country' in post:
        fn = request.POST['fn']
        ln = request.POST['ln']
        email = request.POST['email']
        college = request.POST['college']
        city = request.POST['city']
        country = request.POST['country']
        if fn and ln and email and college and city and country:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': True, 'message': 'User with this email already exists!'})
            else:
                user = User(username=email, first_name=fn, last_name=ln, email=email)
                user.save()

                profile = UserProfile(city=city, country=country, college=college)
                profile.user = user
                profile.save()

                return JsonResponse({'error': False})
        else:
            return JsonResponse({'error': True, 'message': 'empty input field/s'})


    else:
        return JsonResponse({'error': True, 'message': 'not all fields were received'})


def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('http://localhost:8000')


def save_image(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'POST':
        if request.FILES['uncroppedPic']:
            uploaded_file = request.FILES['uncroppedPic']
            try:
                #try opening the image,if it fails then its guranteed that its not an Image
                im = Image.open(uploaded_file)
                if im.format not in ('BMP', 'PNG', 'JPEG'):
                    return HttpResponse("failed")
            except:
                return HttpResponse("failed")

            path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_file.name)
            try:
                with open(path, 'wb+') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
            except Exception as e:
                print str(e)
            return HttpResponse(path)


def crop_image(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    if not user.is_anonymous():
        user_profile = user.user_profile
    if request.method == 'POST':
        if request.POST['url']:
            print "url received"
            x1 = request.POST['x1']
            x2 = request.POST['x2']
            y1 = request.POST['y1']
            y2 = request.POST['y2']
            w = request.POST['w']
            h = request.POST['h']
            try:
                path = request.POST['url']
                im = Image.open(path)
                box = (x1, y1, x2, y2)  #(left, upper, right, lower)
                box = (int(x) for x in box)
                cropped = im.crop(box)
                if not user.is_anonymous():
                    newPath = os.path.join(settings.MEDIA_ROOT, "profile_images", user.username)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath)
                    size = (300, 300)
                    cropped.thumbnail(size)
                    cropped.save(os.path.join(newPath, user.username + "CRPD.jpg"), "jpeg")
                    im.save(os.path.join(newPath, user.username + ".jpg"), "jpeg")
                else:
                    newPath = os.path.join(settings.MEDIA_ROOT, "temp", im)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath)

                    cropped.save(os.path.join(newPath, user.username + "CRPD.jpg"), "jpeg")
                    im.save(os.path.join(newPath, user.username + ".jpg"), "jpeg")

            except Exception as e:
                print str(e)
            return HttpResponse("Success")
        else:
            return HttpResponse("Uh Oh! something went wrong :/")


def thank_you(request):
    #logout user and say thank you :p
    request.session.flush()
    logout(request)
    return render_to_response('user/thankYou.html')


def explore(request):
    return render_to_response('user/explore.html')


@login_required
def get_details(request):
    user = request.user
    details = {}
    userId = request.POST['userId']
    mentee = User.objects.get(id=userId)
    userProfile = user.user_profile
    details["fn"] = mentee.first_name
    details["ln"] = mentee.last_name
    details['pic_url'] = userProfile.picture
    return JsonResponse(details)


@login_required
def root(request):
    """
    Search > Root
    """

    search_query = request.GET.get('q', '')

    # we retrieve the query to display it in the template
    form = MentorSearchForm(request.GET)
    # we call the search method from the MentorSearchForm. Haystack do the work!
    results = form.search()
    return render(request, 'mentee/search_root.html', {
        'search_query': search_query,
        'mentors': results,
    })

#@login_required
#def check_availability(request):
