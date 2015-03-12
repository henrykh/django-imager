from django.forms.models import ModelForm
from imager_images.models import Album, Photo
from imager_images.models import Album
# from django.forms.models import inlineformset_factory


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


class CreateAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('user', None)
        return super(CreateAlbumForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        kwargs['commit'] = False
        obj = super(CreateAlbumForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request
        obj.save()
        return obj

    class Meta:
        model = Album
        fields = ['title', 'description', 'published']



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

# PhotoFormSet = inlineformset_factory(Album, Photo)

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
