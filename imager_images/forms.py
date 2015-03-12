from django.forms.models import ModelForm
from imager_images.models import Album, Photo


class NewAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewAlbumForm, self).__init__(*args, **kwargs)

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


# class PhotoAlbumForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PhotoAlbumForm, self).__init__(*args, **kwargs)

#         # # self.fields['photo'].queryset.filter(user=self.instance.album.user)
#         import pdb; pdb.set_trace()
#         try:
#             self.instance.album
#         except:
#             pass
#         else:
#             self.fields['photo'].queryset = self.fields['photo'].queryset.filter(
#                 user=self.instance.album.user)

#     class Meta:
#          model = Photo.albums.through


class NewPhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude = []


class EditPhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        self.fields['albums'].queryset = self.instance.user.albums.all()

    class Meta:
        model = Photo
        exclude = []


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
