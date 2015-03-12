from django.conf.urls import patterns, url
from imager_images.views import AlbumCreate, AlbumUpdate, AlbumDelete
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
                       # Examples:
                       url(r'library/',
                           'imager_images.views.library', name='library'),
                       url(r'stream/', 'imager_images.views.stream',
                           name='stream'),
                       url(r'album/add/$',
                           login_required(AlbumCreate.as_view()), name='album_add')
                       # url(r'album/(?P<pk>\d+)/$',
                       #     AlbumUpdate.as_view(), name='album_update'),
                       # url(r'album/(?P<pk>\d+)/delete/$',
                       #     AlbumDelete.as_view(), name='album_delete'),
                       )
