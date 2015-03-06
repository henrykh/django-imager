from django.contrib import admin
from models import Album, Photo
from forms import NewAlbumForm, EditAlbumForm, PhotoAlbumForm


class photoAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )


class PhotoInline(admin.TabularInline):
    form = PhotoAlbumForm
    model = Photo.albums.through


class albumAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = NewAlbumForm
        else:
            self.form = EditAlbumForm
        return super(albumAdmin, self).get_form(request, obj, **kwargs)

    list_display = ('title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )
    inlines = [PhotoInline,]

admin.site.register(Album, albumAdmin)
admin.site.register(Photo, photoAdmin)
