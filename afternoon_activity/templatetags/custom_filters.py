from django import template

register = template.Library()

@register.filter(name='concat')
def concat(value, arg):
    """Concatenate arg and value."""
    return str(value) + str(arg)