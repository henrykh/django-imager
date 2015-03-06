from django.contrib import admin
from models import ImagerProfile


class ProfileInline(admin.StackedInline):
    model = ImagerProfile
    fk_name = 'user'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'phone_number',
                    'birthday',
                    'is_active',
                    )


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email'
                    'is_staff'
                    'is_active',
                    'date_joined'
                    )

    inlines = [ProfileInline, ]


admin.site.register(ImagerProfile, ProfileAdmin)
