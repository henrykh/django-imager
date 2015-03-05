from django.contrib import admin
from models import Album, Photo


class albumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description')


class photoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description')

admin.site.register(Album, albumAdmin)
admin.site.register(Photo, photoAdmin)
