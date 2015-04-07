from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from imager_user.views import ProfileUpdateView


urlpatterns = patterns('',
                       url(r'^$', 'imager_user.views.profile',
                           name='profile'),
                       url(r'^update/(?P<pk>\d+)/$',
                           login_required(ProfileUpdateView.as_view()),
                           name='profile_update'),
                       url(r'^(?P<pk>\d+)/$',
                           'imager_user.views.PublicProfile',
                           name='PublicProfile')
                       )
