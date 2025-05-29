from django import template

register = template.Library()

@register.filter
def percent(value):
    try:
        return round(float(value) * 100)
    except (ValueError, TypeError):
        return ''