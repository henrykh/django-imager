from django import forms
import datetime
from django.forms.models import ModelForm
from imager_images.models import Album, Photo
from form_utils.widgets import ImageWidget


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

    class Meta:
        model = Album
        widgets = {'user': forms.HiddenInput, }
        fields = ('user',
                  'title',
                  'description',
                  'published',
                  )

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


class AlbumUpdateViewForm(ModelForm):
    photos = forms.ModelMultipleChoiceField(
        Photo, label='Photos', required=False)
    cover_image = forms.ImageField(
        widget=ImageWidget(template='%(image)s<br />'))

    class Meta:
        model = Album
        fields = ('title',
                  'description',
                  'cover_image',
                  'cover',
                  'date_published',
                  'published')

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            coverImage = kwargs['instance'].cover.image
            kwargs.setdefault('initial', {})['cover_image'] = coverImage

        super(AlbumUpdateViewForm, self).__init__(*args, **kwargs)

        self.fields['photos'].queryset = Photo.objects.filter(
            user=self.instance.user).exclude(albums=self.instance)
        self.fields['cover'].queryset = self.instance.photos.all()
        self.fields['cover_image'].label = 'Cover'

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(AlbumUpdateViewForm, self).save(*args, **kwargs)

        if (obj.published == u'pub' or obj.published == u'shd') and not obj.date_published:
            obj.date_published = datetime.datetime.utcnow()
        else:
            obj.date_published = None

        obj.save()
        obj.photos.add(*self.cleaned_data['photos'])


class PhotoAddViewForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image',
                  'title',
                  'description',
                  'published',
                  ]

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


class PhotoUpdateViewForm(ModelForm):
    class Meta:
        model = Photo
        widgets = {'image': ImageWidget(template='%(image)s<br />')}
        fields = ('image',
                  'albums',
                  'title',
                  'description',
                  'published',
                  )

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
