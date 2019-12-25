from django import template
from django.contrib.auth.models import Group
from datetime import date

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_past_due')
def is_past_due(self, m_date):
    return date.today() <= m_date
