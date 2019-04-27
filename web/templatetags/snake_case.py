from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def snake_case(value: str) -> str:
    return value.replace(' ', '_')
