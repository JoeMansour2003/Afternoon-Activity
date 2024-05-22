from django import template

register = template.Library()

@register.filter(name='concat')
def concat(value, arg):
    """Concatenate arg and value."""
    return str(value) + str(arg)
@register.filter
def filter_by_date(queryset, date):
    return queryset.filter(date=date)
@register.filter
def filter_by_rainy(queryset, rainy_bool):
    return queryset.filter(rainy_day=rainy_bool)