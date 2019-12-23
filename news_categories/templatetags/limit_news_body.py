from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.filter
def body(value):
    end = value.index('</p>')
    return mark_safe(value[:end])