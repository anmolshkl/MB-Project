from django.conf.urls import patterns, url
from apps.user import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^register/$', views.register, name='register'),
                       # url(r'^select/$', views.select, name='select'),
                       url(r'^selectV2/(?P<from_page>.*)/$', views.selectV2, name='selectV2'),
                       url(r'^select/password/$', views.set_password, name='set-password'),
                       url(r'^save-image/$', views.save_image, name='save-image'),
                       url(r'^crop-image/$', views.crop_image, name='crop-image'),
                       url(r'^thank-you/$', views.thank_you, name='thank-you'),
                       url(r'^explore/$', views.explore, name='explore'),
                       url(r'^mail/$', views.sendMail, name='send-email'),
                       url(r'^query/$', views.root, name='root'),
                       url(r'^submit-callLog/$', views.submit_call_log, name='submit call-Log'),
                       url(r'^submit-feedback/$', views.submit_feedback, name='submit feedback'),
                       url(r'^call-valid/$', views.is_call_valid, name='call validity check'),
                       url(r'^confirm/(?P<ak>.*)/$', views.register_confirm, name='register_confirm'),
                       url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
                       url(r'^contact/submit/$', views.contact, name='contact'),
                       url(r'^clear-notifications/$', views.clear_notifications, name='clear-notifications'),
                       url(r'^todo/$', views.handle_todo, name='todo'),
                       url(r'^rebuild-index/$', views.rebuild_index, name='rebuild_index'),
                       )