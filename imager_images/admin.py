from django.contrib import admin
from models import Album, Photo


class albumAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')


class photoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')

admin.site.register(Album, albumAdmin)
admin.site.register(Photo, albumAdmin)
