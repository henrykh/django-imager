from django.forms.models import ModelForm
from imager_user.models import ImagerProfile


class ProfileUpdateViewForm(ModelForm):
    class Meta:
        model = ImagerProfile
        fields = ('follows',
                  'blocking',
                  'picture',
                  'picture_privacy',
                  'birthday',
                  'birthday_privacy',
                  'name_privacy',
                  'email_privacy',
                  )
