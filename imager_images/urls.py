from django.conf.urls import patterns, url
from imager_images.views import AlbumCreate, AlbumUpdate, AlbumDelete
from imager_images.views import PhotoAddView, PhotoUpdateView, PhotoDeleteView, LibraryView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       # Examples:
                       # url(r'library/',
                       #     'imager_images.views.library',
                       #     name='library'),
                       url(r'library/',
                           login_required(LibraryView.as_view()),
                           name='library'),
                       url(r'stream/', 'imager_images.views.stream',
                           name='stream'),
                       url(r'album/add/$',
                           login_required(AlbumCreate.as_view()),
                           name='album_add'),
                       url(r'album/update/(?P<pk>\d+)/$',
                           AlbumUpdate.as_view(),
                           name='album_update'),
                       url(r'album/delete/(?P<pk>\d+)/$',
                           AlbumDelete.as_view(),
                           name='album_delete'),
                       url(r'^photo/add/$',
                           login_required(PhotoAddView.as_view()),
                           name='photo_add'),
                       url(r'^photo/update/(?P<pk>\d+)/$',
                           login_required(PhotoUpdateView.as_view()),
                           name='photo_update'),
                       url(r'^photo/delete/(?P<pk>\d+)/$',
                           login_required(PhotoDeleteView.as_view()),
                           name='photo_delete')
                       )
