from django.conf.urls import patterns, url
from imager_images.views import PhotoAddView, PhotoUpdateView, PhotoDeleteView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       # Examples:
                       url(r'library/',
                           'imager_images.views.library',
                           name='library'),
                       url(r'stream/', 'imager_images.views.stream',
                           name='stream'),
                       url(r'^photo/add/$', login_required(PhotoAddView.as_view()),
                           name='photo_add'),
                       url(r'^photo/update/(?P<pk>\d+)/$', login_required(PhotoUpdateView.as_view()),
                           name='photo_update'),
                       url(r'^photo/delete/(?P<pk>\d+)/$', login_required(PhotoDeleteView.as_view()),
                           name='photo_delete')
                       )
