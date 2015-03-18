from django.conf.urls import patterns, url
from imager_images.views import AlbumAddView, AlbumUpdateView, AlbumDeleteView
from imager_images.views import PhotoAddView, PhotoUpdateView, PhotoDeleteView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'library/',
                           'imager_images.views.library',
                           name='library'),
                       url(r'stream/', 'imager_images.views.stream',
                           name='stream'),
                       url(r'album/add/$',
                           login_required(AlbumAddView.as_view()),
                           name='album_add'),
                       url(r'album/update/(?P<pk>\d+)/$',
                           login_required(AlbumUpdateView.as_view()),
                           name='album_update'),
                       url(r'album/delete/(?P<pk>\d+)/$',
                           login_required(AlbumDeleteView.as_view()),
                           name='album_delete'),
                       url(r'^photo/add/$',
                           login_required(PhotoAddView.as_view()),
                           name='photo_add'),
                       url(r'^photo/update/(?P<pk>\d+)/$',
                           login_required(PhotoUpdateView.as_view()),
                           name='photo_update'),
                       url(r'^photo/delete/(?P<pk>\d+)/$',
                           login_required(PhotoDeleteView.as_view()),
                           name='photo_delete'),
                       url(r'^album/(?P<pk>\d+)/$',
                           'imager_images.views.AlbumPhotoList',
                           name='albumphoto_list'),
                       url(r'^photos/loose/$',
                           'imager_images.views.LoosePhotosList',
                           name='loosephotos_list'),
                       url(r'^photos/all/$',
                           'imager_images.views.AllPhotosList',
                           name='allphotos_list')
                       )
