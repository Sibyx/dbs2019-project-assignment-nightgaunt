from django import template

register = template.Library()


@register.filter('field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


@register.filter('field_template')
def field_template(field):
    return f"_partials/bootstrap/fields/{str(field.field.widget.__class__.__name__).lower()}.html"
