from django.contrib import admin
from models import Album, Photo
from forms import NewAlbumForm, EditAlbumForm
# , PhotoAlbumForm
from django.db import transaction
from django.contrib.admin.options import csrf_protect_m
from sorl.thumbnail import get_thumbnail
from imager import settings
import os


class PhotoAdmin(admin.ModelAdmin):
    def image_thumbnail(self, obj):
        # import pdb; pdb.set_trace()

        if obj.image:
            thumb = get_thumbnail(
                obj.image, "50x50", crop='center', quality=99)
            return '<img src="%s"/>' % (thumb.url)
        else:
            return 'No Image'

    def size(self, obj):
        file_name = '%s/%s' % (settings.MEDIA_ROOT, obj.image.name)
        if os.path.exists(file_name):
            return "%0.1f KB" % (os.path.getsize(file_name)/(1024.0))
        return "0 MB"

    list_display = ('image',
                    'title',
                    'user',
                    'description',
                    'date_uploaded',
                    'date_modified',
                    'date_published',
                    'size'
                    )

    list_filter = ('user',
                   'albums'
                   )
    search_fields = ('user',
                     'user__first_name',
                     'user__last_name',
                     'user__email_name',
                     'albums',
                     'title',
                     'description',
                     'image'
                     )

    readonly_fields = ('image_thumbnail',
                       'date_uploaded',
                       'date_modified',
                       'size'
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

    list_filter = ('user',)
    search_fields = ('user',
                     'user__first_name',
                     'user__last_name',
                     'user__email_name',
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
