from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # Examples:
                       url(r'library/',
                           'imager_images.views.library', name='library'),
                       )
