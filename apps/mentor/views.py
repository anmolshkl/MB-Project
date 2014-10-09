from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.mentor.forms import UserForm, UserProfileForm, EducationForm
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
@login_required
def index(request):
	return HttpResponse("Welcome mentor")



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
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
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

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            education = education_form.save(commit=False)
            education.parent = profile

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            """if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']"""
            # Now we save the UserProfile model instance.
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
        profile_form = UserProfileForm()
        education_form = EducationForm()
    # Render the template depending on the context.
    return render_to_response(
            'mentor/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'education_form': education_form,'registered': registered},
            context)

def self_profile_view(user_object):
    """
    This function returns all the fields 
    for viewing self profile
    """
    context_dict = {}
    user_profile_object = user_object.profile
    # TODO add personal details after the user model
    # is finalized
    
    # initialize all to None
    context_dict['full_name'] = None
    context_dict['gender'] = None
    context_dict['date_of_birth'] = None 
    context_dict['location'] = None 
    context_dict['addresses'] = None 
    context_dict['emails'] = None 
    context_dict['contact_numbers'] = None
    context_dict['employment_details'] = None 
    context_dict['education_details'] = None 
    context_dict['friend_list'] = None
    
    name = user_profile_object.user.get_full_name()
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
    
    address_field = user_profile_object.address_set.all()
    if address_field != None:
        context_dict['addresses'] = address_field
    
    email_field = user_profile_object.emailaddress_set.all()
    if email_field != None:
        temp_email_field = []
        for email in email_field:
            temp_email = {}
            temp_email['email_type'] = email_options[email.email_type]
            temp_email['email_id'] = email.email_id
            temp_email_field.append(temp_email) 
        context_dict['emails'] = temp_email_field
    
    contact_number_field = user_profile_object.contactnumber_set.all()
    if contact_number_field != None:
        temp_contact_number_field = []
        for cn in contact_number_field:
            temp_cn = {}
            temp_cn['number_type'] = contact_options[cn.number_type]
            temp_cn['country_code'] = cn.country_code
            temp_cn['number'] = cn.number
            temp_contact_number_field.append(temp_cn)
        context_dict['contact_numbers'] = temp_contact_number_field
    
    employment_details_field = user_profile_object.employmentdetails_set.all()
    if employment_details_field != None:
        context_dict['employment_details'] = employment_details_field
    
    education_details_field = user_profile_object.educationdetails_set.all()
    if education_details_field != None:
        context_dict['education_details'] = education_details_field
        
    context_dict['friend_list'] = user_profile_object.user.relationships.friends()

    return context_dict
