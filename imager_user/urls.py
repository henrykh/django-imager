from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from imager_user.views import ProfileUpdateView


urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'imager_user.views.profile',
                           name='profile'),
                       url(r'^update/(?P<pk>\d+)/$',
                           login_required(ProfileUpdateView.as_view()),
                           name='profile_update'),
                       # url(r'^update/$', 'imager_user.views.profile_update',
                       #     name='profile_update')
                       )
