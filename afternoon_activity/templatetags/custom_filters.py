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
@register.filter
def primary_cabin(camper, session_number):
    """
    Return the smallest cabin number for this camper in the given session.
    """
    try:
        sc = camper.session_cabin.filter(
            session__session_number=session_number
        ).select_related('cabin').order_by('cabin__cabin_number').first()
        return sc.cabin.cabin_number if sc and sc.cabin else ''
    except Exception:
        return ''

@register.filter
def sort_by_primary_cabin(campers, session_number):
    """
    Sort campers by primary cabin number asc, then last name, then first name.
    campers can be a queryset or list.
    """
    campers_list = list(campers)
    def key(c):
        try:
            sc = c.session_cabin.filter(
                session__session_number=session_number
            ).select_related('cabin').order_by('cabin__cabin_number').first()
            num = sc.cabin.cabin_number if sc and sc.cabin else None
        except Exception:
            num = None
        return (num if isinstance(num, int) else 10**9, getattr(c, 'last_name', ''), getattr(c, 'first_name', ''))
    campers_list.sort(key=key)
    return campers_list