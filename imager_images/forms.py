from django.forms.models import ModelForm
from models import Album


class AlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = self.instance.photos.all()

    class Meta:
        model = Album
        fields = ['user',
                  'title',
                  'description',
                  'date_published',
                  'published',
                  'cover']
