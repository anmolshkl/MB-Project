from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.mentor.forms import UserForm, MentorProfileForm, EducationForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.mentor.models import MentorProfile, EducationDetails,SocialProfiles
from django.contrib.auth.models import User
# Create your views here.
@login_required
def index(request):
	return render_to_response('mentor/index.html',{},RequestContext(request))

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and MentorProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = MentorProfileForm(data=request.POST)
        education_form = EducationForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid() and education_form.is_valid:
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.username = form.cleaned_data['email']
            user.set_password(user.password)
            user.save()

            # Now sort out the MentorProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            education = education_form.save(commit=False)
            education.parent = profile

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the MentorProfile model.
            """if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']"""
            # Now we save the MentorProfile model instance.
            profile.save()
            education.save()
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors,education_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = MentorProfileForm()
        education_form = EducationForm()
    # Render the template depending on the context.
    return render_to_response(
            'mentor/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'education_form': education_form,'registered': registered},
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
    user_profile_object = user.mentor_profile 

    social_profiles_object = SocialProfiles.objects.get(parent=user_profile_object)
    # TODO add personal details after the user model
    # is finalized
    
    # initialize all to None
    context_dict['full_name'] = None
    context_dict['gender'] = None
    context_dict['date_of_birth'] = None 
    context_dict['location'] = None 
    context_dict['country'] = None 
    context_dict['emails'] = None 
    context_dict['contact_numbers'] = None
    context_dict['picture_url'] = None
    context_dict['profile_url'] = None

    gender_options={'male':"M",'female':'F'}

    name = user.first_name + " " + user.last_name
    context_dict['full_name'] = name

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
        context_dict['contact_numbers'] = contact_number_field
    
    picture_url = social_profiles_object.profile_pic_url_linkedin
    if picture_url != None:
        context_dict['picture_url'] = picture_url 

    profile_url = social_profiles_object.profile_url_linkedin
    if profile_url != None:
        context_dict['profile_url'] = profile_url 
    
    return render_to_response("mentor/profile-view.html",context_dict,context)
