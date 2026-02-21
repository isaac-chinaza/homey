from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def short_timesince(value):
    if not value:
        return ""
    time_str = timesince(value)
    return time_str.split(",")[0]