from django import forms
from django.forms.models import ModelForm
from imager_user.models import ImagerProfile
from imager_images.models import Photo
from form_utils.widgets import ImageWidget


class ProfileUpdateViewForm(ModelForm):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email_address = forms.CharField(label='Email Address')

    class Meta:
        model = ImagerProfile
        widgets = {'picture': ImageWidget()}
        fields = ('follows',
                  'blocking',
                  'picture',
                  'picture_privacy',
                  'phone_number',
                  'phone_privacy',
                  'birthday',
                  'birthday_privacy',
                  'first_name',
                  'last_name',
                  'name_privacy',
                  'email_address',
                  'email_privacy',
                  )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            firstName = kwargs['instance'].user.first_name
            kwargs.setdefault('initial', {})['first_name'] = firstName

            lastName = kwargs['instance'].user.last_name
            kwargs.setdefault('initial', {})['last_name'] = lastName

            emailAddress = kwargs['instance'].user.email
            kwargs.setdefault('initial', {})['email_address'] = emailAddress

        super(ProfileUpdateViewForm, self).__init__(*args, **kwargs)

        self.base_fields['follows'].queryset = ImagerProfile.objects.exclude(
            user=kwargs['instance'].user)
        self.base_fields['blocking'].queryset = ImagerProfile.objects.exclude(
            user=kwargs['instance'].user)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(ProfileUpdateViewForm, self).save(*args, **kwargs)
        obj.user.first_name = self.cleaned_data['first_name']
        obj.user.last_name = self.cleaned_data['last_name']
        obj.user.email = self.cleaned_data['email_address']
        new_profile_photo = Photo()
        new_profile_photo.image = self.cleaned_data['picture']
        new_profile_photo.user = obj.user
        new_profile_photo.save()
        obj.user.save()
        obj.save()
        self.save_m2m()
        return obj
