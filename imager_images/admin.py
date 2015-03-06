from django.contrib import admin
from models import Album, Photo
from forms import AlbumForm


class photoAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )


class albumAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ('title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )

admin.site.register(Album, albumAdmin)
admin.site.register(Photo, photoAdmin)
