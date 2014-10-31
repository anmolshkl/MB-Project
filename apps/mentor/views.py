from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from apps.user.forms import UserForm,UserEditForm
from apps.mentor.forms import UserProfileForm, EducationForm, EmploymentForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.user.models import UserProfile,SocialProfiles
from django.contrib.auth.models import User
from random import choice
from string import letters
from apps.mentor.forms import EducationDetailsFormSet,EmploymentDetailsFormSet
from apps.mentor.models import EducationDetails,EmploymentDetails

# Create your views here.

@login_required
def index(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.is_new:
        return render_to_response('user/select.html',{},RequestContext(request))

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
        # Note that we make use of both UserForm and UserProfileForm.
        data = request.POST.copy() # so we can manipulate data
        # random username
        data['username'] = data['email'] #useless,rather keep email as data['email'] username ''.join([choice(letters) for i in xrange(30)])
        data['is_new'] = False
        user_form = UserForm(data)
        profile_form = UserProfileForm(data=request.POST)
        education_form = EducationForm(data=request.POST)
        employment_form = EmploymentForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid() and education_form.is_valid() and employment_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.save()
            '''
            dont need it now
            #now delete the default mentee profile thats created
            UserProfile.objects.get(user=user).delete()
            '''
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_new = False
            profile.is_mentor = True
            education = education_form.save(commit=False)
            education.parent = profile
            employee = employment_form.save(commit=False)
            employee.parent = profile

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            """if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']"""
            # Now we save the UserProfile model instance.
            profile.save()
            education.save()
            employee.save()
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
        employment_form = EmploymentForm()
    # Render the template depending on the context.
    return render_to_response(
            'mentor/register.html',
            {'user_form': user_form, 'profile_form': profile_form,'employment_form': employment_form, 'education_form': education_form,'registered': registered},
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
        return HttpResponseRedirect('user/select.html')
    
    #Social Profile
    try:
        social_profiles_object = SocialProfiles.objects.get(parent=user_profile_object)
    except SocialProfiles.DoesNotExist:
        social_profiles_object = None
    
    #Education Profile 
    try:
        eduObjs = EducationDetails.objects.filter(parent=user_profile_object)
    except EducationDetails.DoesNotExist:
        eduObjs = None
    
    #Employment Profile
    try:
        empObjs = EmploymentDetails.objects.filter(parent=user_profile_object)
    except EmploymentDetails.DoesNotExist:
        empObjs = None
    
    # TODO add personal details after the user model
    # is finalized
    # initialize all to None
    context_dict['full_name'] = None
    context_dict['gender'] = None
    context_dict['date_of_birth'] = None 
    context_dict['location'] = None 
    context_dict['country'] = None 
    context_dict['email'] = None 
    context_dict['contact_number'] = None
    context_dict['about'] = None
    context_dict['provider'] = None
    context_dict['picture_url'] = None
    context_dict['profile_url'] = None
    context_dict['edu_list'] = None
    context_dict['emp_list'] = None

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
    
    contact = user_profile_object.contact
    if contact != None:
        context_dict['contact_number'] = contact
    
    about = user_profile_object.about
    if about:
        context_dict['about'] = about
    
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

        if picture_url != None:
            context_dict['picture_url'] = picture_url 

        if profile_url != None:
            context_dict['profile_url'] = profile_url 
    
    if eduObjs:
        edu_list = []
        for obj in eduObjs:
            edu_list.append({'inst':obj.institution,'loc':obj.location,'degree':obj.degree,
                            'branch':obj.branch,'from':obj.from_year,'to':obj.to_year,'coun':obj.country})

        context_dict['edu_list'] = edu_list

    if empObjs:
        emp_list = []
        for obj in empObjs:
            emp_list.append({'org':obj.organization,'loc':obj.location,'pos':obj.position,
                            'from':obj.from_date,'to':obj.to_date})

        context_dict['emp_list'] = emp_list
    print context_dict
    return render_to_response("mentor/profile-view.html",context_dict,context)

@login_required
def edit_profile(request):
    # The following form method use taken from slide 66 of
    # http://www.slideshare.net/pydanny/advanced-django-forms-usage
    user = request.user
    user_profile = user.user_profile

    if request.POST:
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        #education_detail_formset = EducationDetailFormSet(request.POST, instance=user_profile)
        #employment_detail_formset,created = EmploymentDetailFormSet(request.POST, instance=user_profile)
        edu_formset= EducationDetailsFormSet(request.POST, instance=user_profile)
        emp_formset= EmploymentDetailsFormSet(request.POST, instance=user_profile)
        if form.is_valid() and edu_formset.is_valid() and emp_formset.is_valid():
            user_form.save()
            profile_form.save()
            emp_formset.save()
            edu_formset.save()
            return HttpResponseRedirect("/user/")
            # return here if different behaviour desired
    else:
        user_form = UserEditForm(instance=user)
        form = UserProfileForm(instance=user_profile)
        edu_formset = EducationDetailsFormSet(instance=user_profile)
        emp_formset = EmploymentDetailsFormSet(instance=user_profile)
        '''
        # build a list of all different educational forms from individual education entry
        eduFormList = []
        for edu in EducationDetails.objects.filter(parent=user_profile):
            eduFormList.append(EducationForm(instance=edu))
        
        # build a list of all different Employment forms from individual Employment entry
        empFormList = []
        for emp in EmploymentDetails.objects.filter(parent=user_profile):
            empFormList.append(EmploymentForm(instance=emp))
        '''
        #edu_form = EducationForm(instance=EducationDetails.objects.get_or_create(parent=user_profile)[0])
        #emp_form = EmploymentForm(instance=EmploymentDetails.objects.get_or_create(parent=user_profile)[0])
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
        location = extra_data['location']['name']  #rename address as area
        first_name = extra_data['first-name']
        last_name = extra_data['last-name']
        user.first_name = first_name
        user.last_name = last_name
        (location,country) = location.split(',')
        #date_of_birth = extra_data['date-of-birth'] 
        userProfile = UserProfile.objects.get(user=user)
        userProfile.location = location
        userProfile.country = country
        userProfile.save()
        user.save()
        print "saved user profile" 

        #Save Education Data if received
        if 'educations' in extra_data:
            educations = extra_data['educations']['education']

        if educations:
            for individual_edu in educations:
                print individual_edu['school-name']
                if not EducationDetails.objects.filter(parent=user,institution=individual_edu['school-name']):
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
        socialProfile,created = SocialProfiles.objects.get_or_create(parent=userProfile)
        #socialProfile = SocialProfiles(parent=userProfile)
        socialProfile.profile_url_linkedin = extra_data['public-profile-url']
        socialProfile.profile_pic_url_linkedin = extra_data['picture-url']
        socialProfile.save()
    return HttpResponseRedirect("/mentor/edit-profile/")