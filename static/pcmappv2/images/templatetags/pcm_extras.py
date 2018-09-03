from django.contrib.auth.models import User, Group
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.filter(name=group_name).exists()
    return group
