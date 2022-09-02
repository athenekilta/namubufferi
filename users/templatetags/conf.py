from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def base_url():
    return settings.BASE_URL


@register.simple_tag
def site_name():
    return settings.SITE_NAME