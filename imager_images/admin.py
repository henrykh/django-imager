from django.contrib import admin
from models import Album, Photo
from forms import NewAlbumForm, EditAlbumForm
# , PhotoAlbumForm
from django.db import transaction
from django.contrib.admin.options import csrf_protect_m
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail


class PhotoAdmin(admin.ModelAdmin):
    def image_thumbnail(self, obj):
        if obj.image:
            thumb = get_thumbnail(
                obj.image, "50x50", crop='center', quality=99)
            return u'<img src="%s"/>' % thumb.url
        else:
            return u'image'
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True

    list_display = ('image',
                    'title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )

    list_filter = ('user',
                   'albums'
                   )
    search_fields = ('user',
                     'albums',
                     'title',
                     'description',
                     'image'
                     )

    readonly_fields = ('image_thumbnail',
                       'date_uploaded',
                       'date_modified',
                       )


class PhotoInline(admin.TabularInline):
    # form = PhotoAlbumForm
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

    list_filter = ('user',)
    search_fields = ('user',
                     'title',
                     'description',
                     )

    readonly_fields = ('date_uploaded',
                       'date_modified'
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
