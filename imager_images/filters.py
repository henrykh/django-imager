from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PhotoSizeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('By file size')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'file_size'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('small', _('<= 1 MB')),
            ('medium', _('<= 10 MB')),
            ('large', _('<= 100 MB')),
            ('xlarge', _('> 100 MB')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either 'small', 'medium',
        # 'large', or 'xlarge') to decide how to filter the queryset.
        if self.value() == 'small':
            return queryset.filter(file_size__lte=1048576)
        if self.value() == 'medium':
            return queryset.filter(file_size__lte=10485760)
        if self.value() == 'large':
            return queryset.filter(file_size__lte=104857600)
        if self.value() == 'xlarge':
            return queryset.filter(file_size__gt=104857600)
