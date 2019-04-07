from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def in_list(value, my_list: str) -> bool:
    value = str(value)
    return value in my_list.split(';')
