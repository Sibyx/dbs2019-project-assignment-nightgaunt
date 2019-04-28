from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def wikipedia(value: str) -> str:
    return f"https://en.wikipedia.org/wiki/{value.replace(' ', '_')}"
