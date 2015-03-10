from django.conf.urls import patterns, include, url
from django.contrib import admin
from imager import settings
from django.conf import settings as dcs
from django.conf.urls.static import static

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'imager.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include(
                           'registration.backends.default.urls')),
                       url(r'accounts/profile/',
                           'imager.views.profile', name='profile')
                       )

if settings.DEBUG:
    urlpatterns += static(dcs.MEDIA_URL, document_root=dcs.MEDIA_ROOT)
