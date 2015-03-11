from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # Examples:
                       url(r'library/',
                           'imager_images.views.library', name='library'),
                       url(r'stream/', 'imager_images.views.stream', name='stream')
                       )
