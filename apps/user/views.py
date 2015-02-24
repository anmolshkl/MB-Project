from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import authenticate,login, logout #,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from apps.user.models import UserProfile,SocialProfiles
from apps.mentor.forms import UserProfileForm as MentorProfileForm
from apps.mentee.forms import UserProfileForm as MenteeProfileForm
from apps.mentor.forms import EducationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
#new
#from apps.user.backends import EmailAuthBackend 
from django.conf import settings

from PIL import Image

from allauth.socialaccount.models import SocialAccount
#import magic
# Create your views here.
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


def index(request):
    context_dict = {}
    template = "user/login.html" #default template to render
    user = None
    user_profile = None

    
    if request.user.is_authenticated():
        user_profile,created = UserProfile.objects.get_or_create(user=request.user.id)
    
    #Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/select.html" #User has to select either Mentor/Mentee,so redirect to select.html
        #attach required forms to display in the template

    return render_to_response(template,context_dict,context_instance = RequestContext(request))

def user_login(request):
    # Like before, obtain the context for the user's request.
    print "insedie user_login view"
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                #we 
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the userpage.
                login(request, user)
                return HttpResponseRedirect("/user/thank-you/")
                #return HttpResponseRedirect('/user/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponseRedirect("/user/thank-you/")
                #return HttpResponse("Your Mentor Buddy account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            #return HttpResponse("Invalid login details supplied.")
            return render_to_response('user/login.html', {'error':"Invalid Email/Password"},context_instance = context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GETself.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('user/login.html', {},context_instance = context)
    return render_to_response('user/login.html', {},context_instance = context)



@login_required
def select(request):
    context = RequestContext(request)
    context_dict = {}
    template = "user/select.html"
    if not UserProfile.objects.get(user=request.user).is_new:
        return HttpResponseRedirect('/user/')
    if request.method == 'POST':
        #check whether a request is POST request after submitted choice has come
        if request.POST.get('choice'):
            #store the choice in session for further use
            user = request.user
            user_profile = user.user_profile
            context['selected'] = request.POST['choice']
            template = "user/register.html"
            context_dict['mentor_form'] = MentorProfileForm(instance=user_profile)
            context_dict['mentee_form'] = MenteeProfileForm(instance=user_profile)
            context_dict['education_form'] = EducationForm(instance=user_profile)
        
    return render_to_response(template,context_dict,context)
def register(request):
    post = request.POST #for convenience
    msg=None
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
                return JsonResponse({'error':True,'message':'User with this email already exists!'})
            else:
                user = User(username=email,first_name=fn,last_name=ln,email=email)                
                user.save()

                profile = UserProfile(city=city,country=country,college=college)
                profile.user = user
                profile.save()

                return JsonResponse({'error':False})        
        else:
            return JsonResponse({'error':True,'message':'empty input field/s'})
    

    else:
        return JsonResponse({'error':True,'message':'not all fields were received'})


        
    
'''        
def register(request):
    context = RequestContext(request)
    context_dict = {}
    template  = 'user/register.html'
    user = request.user
    user_profile = user.user_profile
    msg = None
    resume = None
    if not UserProfile.objects.get(user=user).is_new:
        return HttpResponseRedirect("/user/thank-you/")

        #return HttpResponseRedirect('/user/')
    if request.method == 'POST':
        mentor_form = MentorProfileForm(request.POST,request.FILES,instance=user_profile)
        education_form = EducationForm(data=request.POST,instance=user_profile)
        mentee_form = MenteeProfileForm(request.POST,request.FILES,instance=user_profile)
        if request.POST['password1'] != request.POST['password2'] or request.POST['password1'] == '':
            msg = "The confirmation password doesn't matches."
            template = 'user/register.html'
            context_dict['selected'] = request.POST['selected']
            context_dict['error'] = msg
        
        #set the user provided password first so that in case of a mishap user can login again later on 
        #and complete his/her registeration
        if msg == None:
            user.set_password(request.POST["password1"])
            user.save()

        if request.POST['selected'] == 'mentor' and msg == None:
            #the post is for mentor registration, save the form or else display it
            if mentor_form.is_valid() and education_form.is_valid():
                mentor_profile = mentor_form.save(commit=False)
                mentor_profile.user = user
                mentor_profile.is_mentor = True
                mentor_profile.is_new = False
                print request.POST
                if "url" in request.POST:
                    print "url received"
                    cropAndSave(user, request.POST)
                    mentor_profile.picture = request.POST['url']
                else:
                    print "url not received"
                    mentor_profile.picture = (SocialAccount.objects.get(user=user)).get_avatar_url()
                mentor_profile.save()
                education = education_form.save(commit=False)
                education.parent = mentor_profile
                education.save()
                return HttpResponseRedirect("/user/thank-you/")
            
                #return HttpResponseRedirect("/user/")
            
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print mentor_form.errors, education_form.errors

        if request.POST['selected'] == 'mentee' and msg == None:
            #the post is for mentee registration, save the form or else display it
            if mentee_form.is_valid():
               
                mentee_profile = mentee_form.save(commit=False)
                mentee_profile.user = user
                mentee_profile.is_mentor = False
                mentee_profile.is_new = False
                if "url" in request.POST:
                    cropAndSave(user, request.POST)
                    mentee_profile.picture = request.POST['url']
                else:
                    mentee_profile.picture = (SocialAccount.objects.get(user=user)).get_avatar_url()
                mentee_profile.save()
                return HttpResponseRedirect("/user/thank-you/")

                #return HttpResponseRedirect("/user/")            
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print mentee_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        mentor_form = MentorProfileForm(instance=user_profile)
        mentee_form = MenteeProfileForm(instance=user_profile)
        education_form = EducationForm(instance=user_profile)
    # Render the template depending on the context.
    context_dict['selected'] = request.POST['selected']
    context_dict['mentor_form'] =  mentor_form
    context_dict['mentee_form'] =  mentee_form
    context_dict['education_form'] =  education_form
    return render_to_response(template,context_dict,context)
'''


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

            path = os.path.join(settings.MEDIA_ROOT,'temp',uploaded_file.name)
            try:
                with open(path,'wb+') as f:
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
            x1=request.POST['x1']
            x2=request.POST['x2']
            y1=request.POST['y1']
            y2=request.POST['y2']
            w=request.POST['w']
            h=request.POST['h']
            try:
                path = request.POST['url']
                im = Image.open(path)
                box = (x1, y1, x2, y2) #(left, upper, right, lower)
                box = (int(x) for x in box)
                cropped = im.crop(box)
                if not user.is_anonymous(): 
                    newPath = os.path.join(settings.MEDIA_ROOT,"profile_images",user.username)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath)
                    size = (300, 300)
                    cropped.thumbnail(size)
                    cropped.save(os.path.join(newPath,user.username+"CRPD.jpg"),"jpeg")
                    im.save(os.path.join(newPath,user.username+".jpg"),"jpeg")
                else:
                    newPath = os.path.join(settings.MEDIA_ROOT,"temp",im)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath)

                    cropped.save(os.path.join(newPath,user.username+"CRPD.jpg"),"jpeg")
                    im.save(os.path.join(newPath,user.username+".jpg"),"jpeg")

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