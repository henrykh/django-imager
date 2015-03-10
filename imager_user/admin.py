from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.admin.options import csrf_protect_m
from imager_user.models import ImagerProfile


class ProfileInline(admin.StackedInline):
    model = ImagerProfile


class ProfileAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        import pdb; pdb.set_trace()
        if obj:
            return ('user',
                    'follows',
                    'blocking',
                    'picture',
                    'thumbnail',
                    'picture_privacy',
                    'phone_number',
                    'phone_privacy',
                    'birthday',
                    'birthday_privacy',
                    'name_privacy',
                    'email_privacy',
                    )
        else:
            return ('user',
                    'follows',
                    'blocking',
                    'picture',
                    'picture_privacy',
                    'phone_number',
                    'phone_privacy',
                    'birthday',
                    'birthday_privacy',
                    'name_privacy',
                    'email_privacy',
                    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user',
                    )
        else:
            return ()

    def thumbnail(self, obj):
        return obj.picture_thumbnail()

    list_display = ('user',
                    'phone_number',
                    'birthday',
                    'is_active',
                    )


class UserAdmin(UserAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_staff',
                    'is_active',
                    'date_joined'
                    )

    inlines = [ProfileInline, ]

    @csrf_protect_m
    @transaction.atomic
    def changeform_view(
        self, request, object_id=None, form_url='', extra_context=None
    ):
        if not object_id:
            try:
                self.inlines.remove(ProfileInline)
            except ValueError:
                pass
        else:
            if ProfileInline not in self.inlines:
                self.inlines.append(ProfileInline)

        return super(UserAdmin, self).changeform_view(
            request, object_id, form_url, extra_context
            )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ImagerProfile, ProfileAdmin)
