# core/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Return a list of integers from 0 to value-1."""
    return range(value)
