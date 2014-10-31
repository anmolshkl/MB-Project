from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response, render
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

# Create your views here.
@login_required #this is added to avoid SimpleLazyObject request.user error
def index(request):
    context_dict = {}
    template = "user/login.html" #default template to render
    user = request.user
    if user:
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
            context['selected'] = request.POST['choice']
            template = "user/register.html"
            context_dict['mentor_form'] = MentorProfileForm()
            context_dict['mentee_form'] = MenteeProfileForm()
            context_dict['education_form'] = EducationForm()
    return render_to_response(template,context_dict,context)

#register after loggin in through Social App & hence @login_required
@login_required
def register(request):
    context = RequestContext(request)
    user = request.user
    if not UserProfile.objects.get(user=user).is_new:
        return HttpResponseRedirect('/user/')
    if request.method == 'POST':
        mentor_form = MentorProfileForm(data=request.POST)
        education_form = EducationForm(data=request.POST)
        mentee_form = MenteeProfileForm(data=request.POST)
        if request.POST['selected'] == 'mentor':
            #the post is for mentor registration, save the form or else display it
            if mentor_form.is_valid() and education_form.is_valid():
                mentor_profile = mentor_form.save(commit=False)
                mentor_profile.user = user
                mentor_profile.is_mentor = True
                mentor_profile.is_new = False
                mentor_profile.save()
                education = education_form.save(commit=False)
                education.parent = mentor_profile
                education.save()
                return HttpResponseRedirect("/user/")
            
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print mentor_form.errors, education_form.errors

        if request.POST['selected'] == 'mentee':
            print "mentee data received"
            #the post is for mentee registration, save the form or else display it
            if mentee_form.is_valid():
                print "mentee data correct"
                mentee_profile = mentee_form.save(commit=False)
                mentee_profile.user = user
                mentee_profile.is_mentor = False
                mentee_profile.is_new = False
                mentee_profile.save()
                return HttpResponseRedirect("user/login.html")            
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print mentee_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        mentor_form = MentorProfileForm()
        mentee_form = MenteeProfileForm()
        education_form = EducationForm()
    # Render the template depending on the context.
    return render_to_response('user/select.html',{'selected':request.POST['selected'],'mentor_form': mentor_form, 'mentee_form': mentee_form, 'education_form': education_form},context)



def user_logout(request):
        request.session.flush()
        logout(request)
        return HttpResponseRedirect('/user/')


