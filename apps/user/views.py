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
#new
#from apps.user.backends import EmailAuthBackend 
from django.conf import settings

from PIL import Image

# Create your views here.
import os
def index(request):
    context_dict = {}
    template = "user/login.html" #default template to render
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

    return render_to_response(template,context_dict,RequestContext(request))

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        email = request.POST['email']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        '''
        backend_obj = EmailAuthBackend()
        user = backend_obj.authenticate(username=email, password=password)
        '''
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        user = authenticate(username=email, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                #we 
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the userpage.
                login(request, user)
                return HttpResponseRedirect('/user/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Mentor Buddy account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GETself.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('user/login.html', {}, context)


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
            print "entered"
            #store the choice in session for further use
            user = request.user
            user_profile = user.user_profile
            context['selected'] = request.POST['choice']
            template = "user/register.html"
            context_dict['mentor_form'] = MentorProfileForm(instance=user_profile)
            context_dict['mentee_form'] = MenteeProfileForm(instance=user_profile)
            context_dict['education_form'] = EducationForm(instance=user_profile)
            
            #return HttpResponseRedirect('/user/register/?selected=%s'%(request.POST['choice']))
    return render_to_response(template,context_dict,context)

#register after loggin in through Social App & hence @login_required
@login_required
def register(request):
    context = RequestContext(request)
    context_dict = {}
    template  = 'user/register.html'
    user = request.user
    user_profile = user.user_profile
    print 'entered register'
    msg = None
    if not UserProfile.objects.get(user=user).is_new:
        return HttpResponseRedirect("/user/thank-you/")

        #return HttpResponseRedirect('/user/')
    if request.method == 'POST':
        mentor_form = MentorProfileForm(request.POST,request.FILES,instance=user_profile)
        education_form = EducationForm(data=request.POST,instance=user_profile)
        mentee_form = MenteeProfileForm(request.FILES,request.POST,instance=user_profile)
        if request.POST['password1'] != request.POST['password2'] or request.POST['password1'] == '':
            msg = "The confirmation password doesn't matches."
            template = 'user/register.html'
            context_dict['selected'] = request.POST['selected']
            context_dict['error'] = msg

        if request.POST['selected'] == 'mentor' and msg == None:
            #the post is for mentor registration, save the form or else display it
            print 'mentor data received'
            if mentor_form.is_valid() and education_form.is_valid():
                #print 'mentor data valid'
                #print request.POST
                #print request.FILES
                mentor_profile = mentor_form.save(commit=False)
                mentor_profile.user = user
                mentor_profile.is_mentor = True
                mentor_profile.is_new = False
                #mentor_profile.picture = request.FILES['picture']
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



def user_logout(request):
        request.session.flush()
        logout(request)
        return redirect('http://localhost:8000')

@login_required
def save_image(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    user_profile = user.user_profile
    if request.method == 'POST':
        if request.FILES['uncroppedPic']:
            print "received"
            uploaded_file = request.FILES['uncroppedPic']
            print 'assigned'
            path = os.path.join(settings.MEDIA_ROOT,'temp',uploaded_file.name)
            try:
                with open(path,'wb+') as f:
                    print 'opened'
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
            except Exception as e:
                print str(e)
            return HttpResponse(path)

def crop_image(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    user_profile = user.user_profile
    if request.method == 'POST':
        if request.POST['url']:
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

                newPath = os.path.join(settings.MEDIA_ROOT,"profile_images",user.username)
                if not os.path.exists(newPath):
                    os.makedirs(newPath)

                cropped.save(os.path.join(newPath,user.username+"CRPD"),"jpeg")
                im.save(os.path.join(newPath,user.username),"jpeg")
                print "image saved"
            except Exception as e:
                print str(e)
            return HttpResponse("Success")
        else:
            return HttpResponse("Uh Oh! something went wrong :/")
@login_required
def thank_you(request):
    return render_to_response('user/thankYou.html')

def explore(request):
    return render_to_response('user/explore.html')