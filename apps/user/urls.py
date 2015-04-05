from django.conf.urls import patterns, url
from apps.user import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^select/$', views.select, name='select'),
                       url(r'^select/password/$', views.set_password, name='set-password'),
                       url(r'^save-image/$', views.save_image, name='save-image'),
                       url(r'^crop-image/$', views.crop_image, name='crop-image'),
                       url(r'^thank-you/$', views.thank_you, name='thank-you'),
                       url(r'^explore/$', views.explore, name='explore'),
                       url(r'^getDetails/$', views.get_details, name='get-details'),
                       url(r'^mail/$', views.sendMail, name='send-email'),
                       url(r'^query/$', views.root, name='root'),
                       url(r'^submit-callLog/$', views.submit_call_log, name='submit call-Log'),
                       url(r'^submit-feedback/$', views.submit_feedback, name='submit feedback'),
                       url(r'^call-valid/$', views.is_call_valid, name='call validity check'),
                       url(r'^confirm/$', views.register_confirm, name='register_confirm'),
                       )