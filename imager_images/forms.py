from django import forms
import datetime
from django.forms.models import ModelForm
from imager_images.models import (Album,
                                  Photo
                                  )


class NewAlbumAdminForm(ModelForm):

    class Meta:
        model = Album
        exclude = []


class NewPhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = []


class EditPhotoAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPhotoAdminForm, self).__init__(*args, **kwargs)
        self.fields['albums'].queryset = self.instance.user.albums.all()

    class Meta:
        model = Photo
        exclude = []


class AlbumAddViewForm(ModelForm):
    photos = forms.ModelMultipleChoiceField(
        Photo, label='Photos', required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumAddViewForm, self).__init__(*args, **kwargs)
        user = self.initial.get('user')
        self.fields['photos'].queryset = Photo.objects.filter(user=user)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(AlbumAddViewForm, self).save(*args, **kwargs)
        obj.save()
        obj.photos.add(*self.cleaned_data['photos'])
        return obj

    class Meta:
        model = Album
        widgets = {'user': forms.HiddenInput, }
        fields = ('user',
                  'title',
                  'description',
                  'published',
                  )


class AlbumUpdateViewForm(ModelForm):
    photos = forms.ModelMultipleChoiceField(
        Photo, label='Photos', required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumUpdateViewForm, self).__init__(*args, **kwargs)
        # import ipdb; ipdb.set_trace()
        self.fields['photos'].queryset = Photo.objects.filter(
            user=self.instance.user).exclude(albums=self.instance)
        self.fields['cover'].queryset = self.instance.photos.all()

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(AlbumUpdateViewForm, self).save(*args, **kwargs)

        if (obj.published == u'pub' or obj.published == u'shd') and not obj.date_published:
            obj.date_published = datetime.datetime.utcnow()
        else:
            obj.date_published = None

        obj.save()
        obj.photos.add(*self.cleaned_data['photos'])

    class Meta:
        model = Album
        fields = ('title',
                  'description',
                  'cover',
                  'date_published',
                  'published')


class PhotoAddViewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)
        return super(PhotoAddViewForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(PhotoAddViewForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request
        obj.save()
        return obj

    class Meta:
        model = Photo
        fields = ['image',
                  'title',
                  'description',
                  'published',
                  ]


class PhotoUpdateViewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoUpdateViewForm, self).__init__(*args, **kwargs)
        self.fields['albums'].queryset = self.instance.user.albums.all()

    def save(self, *args, **kwargs):
        kwargs['commit'] = False

        obj = super(PhotoUpdateViewForm, self).save(*args, **kwargs)
        if (obj.published == u'pub' or obj.published == u'shd') and not obj.date_published:
            obj.date_published = datetime.datetime.utcnow()
        else:
            obj.date_published = None

        obj.save()
        self.save_m2m()

    class Meta:
        model = Photo

        fields = ('albums',
                  'title',
                  'description',
                  'published',
                  )

# class AlbumUpdateViewForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(AlbumUpdateViewForm, self).__init__(*args, **kwargs)
#         # import ipdb; ipdb.set_trace()
#         self.fields['photos'].queryset = self.instance.user.photos.all()

#     class Meta:
#         model = Album

#         fields = ('title',
#                   'description',
#                   'photos',
#                   'published'
#                   )


# class PhotoAlbumForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PhotoAlbumForm, self).__init__(*args, **kwargs)

#         # # self.fields['photo'].queryset.filter(user=self.instance.album.user)
#         import pdb; pdb.set_trace()
#         try:
#             self.instance.album
#         except:
#             pass
#         else:'photo'].queryset = self.fields['photo'].queryset.filter(
#                 user=self.instance.album.user)

#     class Meta:
#          model = Photo.albums.through
