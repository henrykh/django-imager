from django.forms.models import ModelForm
from models import Album, Photo


class NewAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewAlbumForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Album


class EditAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = self.instance.photos.all()
        # self.fields['photos'].queryset = self.instance.user.photos.all()

    class Meta:
        model = Album

# class PhotoAlbumForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PhotoAlbumForm, self).__init__(*args, **kwargs)

#         # # self.fields['photo'].queryset.filter(user=self.instance.album.user)
#         # import pdb; pdb.set_trace()
#         self.fields['photo'].queryset = self.fields['photo'].queryset.filter(
#              user=self.instance.album.user)

 
#     class Meta:
#          model = Photo.albums.through


class NewPhotoForm(ModelForm):
    class Meta:
        model = Photo


class EditPhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        self.fields['albums'].queryset = self.instance.user.albums.all()

    class Meta:
        model = Photo
