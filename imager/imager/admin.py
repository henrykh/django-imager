from django.contrib import admin
from models import profile


class profileAdmin(admin.ModelAdmin):
    fields = ['user', 'is_active']

admin.site.register(profile, profileAdmin)
