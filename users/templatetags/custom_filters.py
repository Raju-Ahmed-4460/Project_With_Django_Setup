from django import template
from datetime import datetime
from django.utils import timezone

register=template.Library()

@register.filter

def humanized_date(value):
    if value:
        today=timezone.localdate()
        value=timezone.localtime(value)
        if value.date() == today:
            return f"Today at:{value.strftime('%I:%M %p')}"
        return value.strftime('%d %B %Y at %I:%M %p')