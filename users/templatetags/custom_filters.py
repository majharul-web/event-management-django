from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def format_date(value):
    if value:
        today = datetime.now().date()
        value=timezone.localtime(value)
        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date() == today.replace(day=today.day - 1):
            return f"Yesterday at {value.strftime('%I:%M %p')}"
        else:
            return f"{value.date()} at {value.strftime('%I:%M %p')}"
    return "No login data available"

@register.filter
def not_in_group(user, group_name):
    return not user.groups.filter(name=group_name).exists()