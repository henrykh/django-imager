from django.contrib import admin
from django.db import transaction
from django.contrib.admin.options import csrf_protect_m
from imager_images.filters import PhotoSizeFilter
from imager_images.forms import *
from imager_images.models import Album, Photo
from sorl.thumbnail import get_thumbnail


class PhotoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = NewPhotoForm
        else:
            self.form = EditPhotoAdminForm
        return super(PhotoAdmin, self).get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if obj:
            return ('user',
                    'image',
                    'thumbnail',
                    'albums',
                    'title',
                    'description',
                    'date_published',
                    'published',
                    'date_uploaded',
                    'date_modified',
                    'size',
                    )
        else:
            return ('user',
                    'image',
                    'title',
                    'description',
                    'date_published',
                    'published',
                    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user',
                    'thumbnail',
                    'date_uploaded',
                    'date_modified',
                    'size'
                    )
        else:
            return ()

    def thumbnail(self, obj):
        if obj.image:
            thumb = get_thumbnail(
                obj.image, "100x100", crop='center', quality=99)
            return '<img src="%s"/>' % (thumb.url)
        else:
            return 'No Image'

    thumbnail.short_description = 'Image Thumbnail'
    thumbnail.allow_tags = True

    def user_linked(self, obj):
        return '<a href=%s%s>%s</a>' % (
            '/admin/auth/user/', obj.user.pk, obj.user)
    user_linked.allow_tags = True
    user_linked.short_description = 'User'

    def size(self, obj):
            if obj.image.size <= 1024:
                return "{:0.1f} B".format(obj.file_size)
            if obj.image.size <= 1024.0**2:
                return "{:0.1f} KB".format(obj.file_size/1024.0)
            if obj.image.size <= 1024.0**3:
                return "{:0.1f} MB".format(obj.file_size/(1024.0**2))
            if obj.image.size <= 1024.0**4:
                return "{:0.1f} GB".format(obj.file_size/(1024.0**3))
            return "0 MB"

    list_display = ('image',
                    'title',
                    'description',
                    'user_linked',
                    'published',
                    'date_uploaded',
                    'date_modified',
                    'date_published',
                    'size'
                    )

    list_filter = ('user',
                   'albums',
                   PhotoSizeFilter,
                   )

    search_fields = ('user__username',
                     'user__first_name',
                     'user__last_name',
                     'user__email',
                     'albums__title',
                     'albums__description',
                     'title',
                     'description'
                     )


class PhotoInline(admin.TabularInline):
    model = Photo.albums.through

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(PhotoInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        field.queryset = field.queryset.filter(user=request._obj_.user)
        return field


class AlbumAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        if not obj:
            self.form = NewAlbumAdminForm
        else:
            self.form = EditAlbumForm
        return super(AlbumAdmin, self).get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if obj:
            return ('user',
                    'title',
                    'description',
                    'cover',
                    'thumbnail',
                    'date_published',
                    'published',
                    'date_uploaded',
                    'date_modified',
                    )
        else:
            return ('user',
                    'title',
                    'description',
                    'date_published',
                    'published',
                    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user',
                    'thumbnail',
                    'date_uploaded',
                    'date_modified',
                    )
        else:
            return ()

    def thumbnail(self, obj):
        if obj.cover.image:
            thumb = get_thumbnail(
                obj.cover.image, "100x100", crop='center', quality=99)
            return '<img src="%s"/>' % (thumb.url)
        else:
            return 'No Image'

    thumbnail.short_description = 'Cover Thumbnail'
    thumbnail.allow_tags = True

    def user_linked(self, obj):
        return '<a href=%s%s>%s</a>' % (
            '/admin/auth/user/', obj.user.pk, obj.user)

    user_linked.allow_tags = True
    user_linked.short_description = 'User'

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

    list_display = ('title',
                    'description',
                    'user_linked',
                    'published',
                    'date_uploaded',
                    'date_modified',
                    'date_published'
                    )

    list_filter = ('user',)
    search_fields = ('user__username',
                     'user__first_name',
                     'user__last_name',
                     'user__email',
                     'title',
                     'description',
                     )

    readonly_fields = ('user',
                       'date_uploaded',
                       'date_modified'
                       )

    inlines = [PhotoInline, ]

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
