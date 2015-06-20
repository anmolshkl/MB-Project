from decimal import Decimal
import hashlib
import random
from apps.mentee.models import Credits
from apps.mentor.models import Ratings
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout  # ,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from apps.user.models import UserProfile, SocialProfiles, MentorSearchForm, Request, CallLog, Feedback, \
    VerificationCodes, Notification, Todo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# new
# from apps.user.backends import EmailAuthBackend
from django.conf import settings

from PIL import Image

# import magic
# Create your views here.
from django.core.mail import send_mail
from django.utils import timezone
from mentorbuddy.settings import SITE_URL
import pytz, datetime


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


def index(request):
    context_dict = {}
    template = "user/loginV3.html"  # default template to render
    user = None
    user_profile = None

    if request.user.is_authenticated():
        user_profile, created = UserProfile.objects.get_or_create(user=request.user.id)

    # Check whether the user is new,if yes then he needs to select btw Mentor-Mentee
    if user_profile and user_profile.is_new:
        context_dict['selected'] = None
        template = "user/select.html"  # User has to select either Mentor/Mentee,so redirect to select.html
        # attach required forms to display in the template

    if user_profile and not user_profile.is_new:
        if user_profile.is_mentor == True:
            return HttpResponseRedirect("/mentor/")
        else:
            return HttpResponseRedirect("/mentee/")

    return render_to_response(template, context_dict, context_instance=RequestContext(request))


def user_login(request):
    error = False
    msg = None
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
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                (social_profile, created) = SocialProfiles.objects.get_or_create(parent=user_profile)
            else:
                error = True
                msg = "Your account is not active. Please contact the admin."
        else:
            error = True
            msg = "Please check your email/password."

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GETself.
    else:
        error = True
        msg = "Not a POST request."
    return JsonResponse({"error": error, "msg": msg})


def select(request):
    error = False
    msg = None
    template = "user/select.html"
    user = request.user
    user_profile = user.user_profile

    if not UserProfile.objects.get(user=request.user).is_new:
        return HttpResponseRedirect('/user/')

    if request.method == 'POST':
        # check whether a request is POST request after submitted choice has come
        if 'choice' in request.POST:
            if request.POST['choice'] == "mentor":
                user_profile.is_mentor = True
                user_profile.save()
                # create new notification
                notif_obj = Notification.objects.create(to=user)
                notif_obj.frm = "admin"
                notif_obj.text = "We appreciate your effort to help someone treading your path!<br>Go and be a super " \
                                 "mentor! :)"
                notif_obj.title = "Hello Mentor!"
                notif_obj.save()
                # sameer


            elif request.POST['choice'] == "mentee":
                user_profile.is_mentor = False
                credits_obj = Credits.objects.create(parent=user)
                credits_obj.save()
                user_profile.save()
                # create new notification
                notif_obj = Notification.objects.create(to=user)
                notif_obj.frm = "admin"
                notif_obj.text = "We'll help you get started with your dream of global education"
                notif_obj.title = "Hello Mentee!"
                notif_obj.save()
                # sameer

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
        # check whether a request is POST request after submitted choice has come
        if 'password' in request.POST and 'confirmPassword' in request.POST:
            if request.POST['password'] == request.POST['confirmPassword'] and request.POST['password'] != '':
                if len(request.POST['password']) >= 6:
                    user.set_password(request.POST['password'])
                    user.save()

                    # check if it's a new user
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
    post = request.POST  # for convenience
    msg = None
    # check if we got all the input fields
    if request.method == 'POST' and 'fn' in post and 'ln' in post and 'email' in post and 'college' in post and 'city' in post and 'country' in post:
        fn = request.POST['fn']
        ln = request.POST['ln']
        email = request.POST['email']
        college = request.POST['college']
        city = request.POST['city']
        country = request.POST['country']
        if fn and ln and email and college and city and country:
            if User.objects.filter(email=email).exists():
                print "email="
                print email
                return JsonResponse({'error': True, 'message': 'User with this email already exists!'})
            else:
                username = email[0:29]
                user = User(username=username, first_name=fn, last_name=ln, email=email)
                user.save()

                profile = UserProfile(city=city, country=country, college=college)
                profile.user = user
                profile.timezone = request.visitor['location']['timezone']
                profile.save()




                # generate key

                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt + email).hexdigest()
                key_expires = datetime.datetime.now(pytz.utc) + datetime.timedelta(days=2)

                # save key

                new_key = VerificationCodes(user=user, activation_key=activation_key, key_expires=key_expires)
                new_key.save()

                # Send email with activation key
                email_subject = 'Account confirmation'
                email_body = "Hey " + fn + ", thanks for signing up.<br> To activate your account, click this link within 48 hours: <br>" + settings.SITE_URL + "user/confirm/" + activation_key
                print "trying to send mail with activation key"
                send_mail(email_subject, email_body, 'anmol@mentorbuddy.in', [email], fail_silently=False)
                print "mail sent with activation key"
                return JsonResponse({'error': False})
        else:
            return JsonResponse({'error': True, 'message': 'empty input field/s'})

    else:
        return JsonResponse({'error': True, 'message': 'not all fields were received'})


def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect(SITE_URL)


def save_image(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'POST':
        if request.FILES['uncroppedPic']:
            uploaded_file = request.FILES['uncroppedPic']
            try:
                # try opening the image,if it fails then its guranteed that its not an Image
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
                box = (x1, y1, x2, y2)  # (left, upper, right, lower)
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
    # logout user and say thank you :p
    request.session.flush()
    logout(request)
    return render_to_response('user/thankYou.html')


def explore(request):
    return render_to_response('user/explore.html')


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
    print results
    return render(request, 'mentee/search_root.html', {
        'search_query': search_query,
        'mentors': results,
    })


def get_utc_time(request, time):
    # first we need to convert this local time to UTC time
    time_zone = pytz.timezone(request.user.user_profile.timezone)
    # get naive date
    date = datetime.datetime.now().date()
    # get naive time
    time = datetime.time(int(time.split(":")[0]), int(time.split(":")[1]), int(time.split(":")[2]))
    date_time = datetime.datetime.combine(date, time)
    # make time zone aware
    date_time = time_zone.localize(date_time)
    # convert to UTC
    utc_date_time = date_time.astimezone(pytz.utc)
    # get time
    return utc_date_time.time()


@login_required
def submit_call_log(request):
    error = False
    msg = None
    request_id = None
    if request.method == 'POST':
        post = request.POST
        if 'request_id' in post and 'end_time' in post and 'est_time' in post and 'end_cause' in post and 'duration' in post:
            if post['request_id'] != '' and post['end_time'] != '' and post[
                'end_cause'] != '' and post['duration'] != '' and post['est_time'] != '':
                request_obj = Request.objects.get(id=post['request_id'])
                request_id = post['request_id']
                utc_est_time = get_utc_time(request, post['est_time'])
                utc_end_time = get_utc_time(request, post['end_time'])
                (call_obj, created) = CallLog.objects.get_or_create(request=request_obj)
                # if any of the speaker has intentionally disconnected, we need to mark request as fulfilled
                if post['end_cause'] == 'HUNG_UP':
                    request_obj.is_completed = True
                    request_obj.save()
                if created:
                    call_obj.establishedTime = utc_est_time
                    call_obj.endTime = utc_end_time
                    # Round off secs
                    call_obj.duration = int(Decimal(post['duration']))
                else:
                    call_obj.duration += int(Decimal(post['duration']))
                    call_obj.endTime = utc_end_time
                call_obj.endCause = post['end_cause']
                call_obj.save()
            else:
                error = True
                msg = "Received empty fields"
        else:
            error = True
            msg = "Missing fields"
    else:
        error = True
        msg = "Not a Post Request"

    return JsonResponse({'error': error, 'msg': msg, 'request_id': request_id})


@login_required
def submit_feedback(request):
    error = False
    msg = None
    if request.method == 'POST':
        post = request.POST
        if 'request_id' in post and 'rating' in post and 'feedback' in post:
            if post['rating'] != '' and post['request_id'] != '':
                request_obj = Request.objects.get(id=int(post['request_id']))
                call_log_obj = request_obj.callLog
                feedback_obj = Feedback(user=request.user)
                feedback_obj.call = call_log_obj
                feedback_obj.rating = post['rating']
                feedback_obj.feedback = post['feedback']

                (rating_obj, created) = Ratings.objects.get_or_create(mentor=request_obj.mentorId)
                rating_obj.average = (rating_obj.average*rating_obj.count+int(post['rating']))/(rating_obj.count+1)
                rating_obj.count += 1
                if post['rating'] == '1':
                    rating_obj.one += 1
                elif post['rating'] == '2':
                    rating_obj.two += 1
                elif post['rating'] == '3':
                    rating_obj.three += 1
                elif post['rating'] == '4':
                    rating_obj.four += 1
                elif post['rating'] == '5':
                    rating_obj.five += 1
                rating_obj.save()
                feedback_obj.save()
            else:
                error = True
                msg = "Received empty fields"
        else:
            error = True
            msg = "Missing fields"
    else:
        error = True
        msg = "Not a Post Request"

    return JsonResponse({'error': error, 'msg': msg})


def is_call_valid(request):
    request_obj = Request.objects.get(id=request.GET['request_id'])
    try:
        call_obj = CallLog.objects.get(request=request_obj)
    except CallLog.DoesNotExist:
        call_obj = None
    valid = True
    if request_obj and call_obj:
        if call_obj.duration >= 1800 or request_obj.is_completed is True:
            valid = False

    return HttpResponse(valid)


def register_confirm(request, ak):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    verification_obj = get_object_or_404(VerificationCodes, activation_key=ak)
    # ver_obj = VerificationCodes.objects.get(activation_key=activation_key)
    # check if the activation key has expired, if it has then render confirm_expired.html

    print verification_obj.key_expires
    print timezone.now()
    if verification_obj.key_expires < timezone.now():
        print "the activation key has expired"
        return redirect('/user/')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = verification_obj.user
    user.is_active = True
    user.save()
    print "user email confirmed"
    # small hack, since we do not call authenticate() on user we need to manually set the backend
    # which has authenticated it
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('/user/')


def contact(request):
    error = False
    msg = None
    if request.method == "POST":
        if "name" in request.POST and "email" in request.POST and "query" in request.POST:
            if request.POST['name'] != '' and request.POST['email'] != '' and request.POST['query'] != '':
                send_mail("New query from " + request.POST['name'],
                          request.POST['query'] + "\n - " + request.POST['name'] + "\n" + request.POST['email'],
                          "anmol@mentorbuddy.in", ["anmol@mentorbuddy.in"], fail_silently=False)
            else:
                error = True
                msg = "Input fields can't be empty!"
        else:
            error = True
            msg = "Missing fields"
    else:
        error = True
        msg = "Submit form using a POST method"

    return JsonResponse({'error': error, "msg": msg})


@login_required
def clear_notifications(request):
    error = False
    if request.GET:
        try:
            Notification.objects.filter(to=request.user).delete()
        except ObjectDoesNotExist:
            error = True
    return JsonResponse({"error": error})


@login_required
def handle_todo(request):
    error = False
    obj_id = None
    if request.method == 'POST':
        if 'delete' in request.POST:
            Todo.objects.filter(id=int(request.POST['id'])).delete()
        elif 'add' in request.POST:
            todo_obj = Todo.objects.create(parent=request.user)
            todo_obj.task = request.POST['task']
            todo_obj.save()
            obj_id = todo_obj.id
        else:
            error = True
    else:
        error = True
    return JsonResponse({"error": error, 'id': obj_id})





