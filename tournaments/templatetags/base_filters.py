from django import template

register = template.Library()


@register.filter
def first_part(value):
    return value.split('_')[0]

@register.filter
def index(dict, i):
    return dict.get(int(i), '')

@register.filter
def filter(dict, i):
    return dict.filter(type=i)