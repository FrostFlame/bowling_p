from django import template

register = template.Library()


@register.filter
def first_part(value):
    return value.split('_')[0]