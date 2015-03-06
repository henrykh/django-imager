from django.contrib import admin
from models import Album, Photo
from forms import NewAlbumForm, EditAlbumForm, PhotoAlbumForm
from django.db import transaction
from django.contrib.admin.options import csrf_protect_m


class PhotoAdmin(admin.ModelAdmin):
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


class AlbumAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = NewAlbumForm
        else:
            self.form = EditAlbumForm
        return super(AlbumAdmin, self).get_form(request, obj, **kwargs)

    list_display = ('title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )

    inlines = [PhotoInline, ]

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(
        self, request, object_id=None, form_url='', extra_context=None
    ):
        if not object_id:
            try:
                self.inlines.remove(PhotoInline)
            except ValueError:
                pass
        else:
            if PhotoInline not in self.inlines:
                self.inlines.append(PhotoInline)

        return super(AlbumAdmin, self).changeform_view(
            request, object_id, form_url, extra_context
            )

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
