from django.contrib import admin
from models import ImagerProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = ImagerProfile


class ProfileAdmin(admin.ModelAdmin):
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

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ImagerProfile, ProfileAdmin)
