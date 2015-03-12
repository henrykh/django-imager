from django.conf.urls import patterns, include, url
from django.contrib import admin
from imager import settings
from django.conf import settings as dcs
from django.conf.urls.static import static

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'imager.views.home', name='home'),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include(
                           'registration.backends.default.urls')),
                       url(r'^profile/', include(
                           'imager_user.urls', namespace='profile')),
                       url(r'^', include(
                           'imager_images.urls', namespace='images'))
                       )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(dcs.MEDIA_URL, document_root=dcs.MEDIA_ROOT)
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),)
