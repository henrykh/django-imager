from django.contrib import admin
from models import ImagerProfile


class profileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'phone_number',
                    'birthday',
                    'is_active',
                    )

admin.site.register(ImagerProfile, profileAdmin)
