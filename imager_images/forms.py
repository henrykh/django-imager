from django.forms.models import ModelForm
from models import Album, Photo


class NewAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewAlbumForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Album
        fields = ['user',
                  'title',
                  'description',
                  'date_published',
                  'published']


class EditAlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = self.instance.photos.all()

    class Meta:
        model = Album
        fields = ['user',
                  'title',
                  'description',
                  'date_published',
                  'published',
                  'cover']


class PhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = self.instance.user.albums.all()

    class Meta:
        model = Photo
        fields = ['user',
                  'image',
                  'albums',
                  'title',
                  'description',
                  'date_published',
                  'published']
