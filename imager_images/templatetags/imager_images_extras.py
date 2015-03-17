from django import template

register = template.Library()


@register.filter(name='random_cover')
def random_cover(value):
    return value.order_by('?')[0].image
