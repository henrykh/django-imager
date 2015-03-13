from django.forms.models import ModelForm
from imager_images.models import (Album,
                                  Photo
                                  )


class NewAlbumAdminForm(ModelForm):

    class Meta:
        model = Album
        exclude = []


class EditAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = self.instance.photos.all()
        # self.fields['photos'].queryset = self.instance.user.photos.all()

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


class CreateAlbumViewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)
        return super(CreateAlbumViewForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(CreateAlbumViewForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request
        obj.save()
        return obj

    class Meta:
        model = Album
        fields = ['title', 'description', 'published']


class CreatePhotoViewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)
        return super(CreatePhotoViewForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace();
        kwargs['commit'] = False
        obj = super(CreatePhotoViewForm, self).save(*args, **kwargs)
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
        # import ipdb; ipdb.set_trace()
        self.fields['albums'].queryset = self.instance.user.albums.all()

    class Meta:
        model = Photo

        fields = ('albums',
                  'title',
                  'description',
                  'date_published',
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
