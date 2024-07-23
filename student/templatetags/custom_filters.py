from django import template

register = template.Library()


@register.filter
def comma_to_dot(value):
    return str(value).replace(',', '.')


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    request = context['request']
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()


@register.filter
def subtract(value, arg):
    return value - arg if value and arg else value or 0
