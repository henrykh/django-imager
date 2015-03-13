from django import forms
from django.forms.models import ModelForm
from imager_user.models import ImagerProfile


class ProfileUpdateViewForm(ModelForm):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email_address = forms.CharField(label='Email Address',)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            import ipdb; ipdb.set_trace()
            firstName = kwargs['instance'].user.first_name
            kwargs.setdefault('initial', {})['first_name'] = firstName

            lastName = kwargs['instance'].user.last_name
            kwargs.setdefault('initial', {})['last_name'] = lastName

            email = kwargs['instance'].user.email
            kwargs.setdefault('initial', {})['email_address'] = email

        return super(ProfileUpdateViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ImagerProfile
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
