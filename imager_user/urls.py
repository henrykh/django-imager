from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'imager_user.views.profile', name='profile'),
                       url(r'^edit/$', 'imager_user.views.profile_edit', name='profile_edit')
                       )
