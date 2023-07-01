from django import template
from datetime import datetime, timedelta

# 시간 계산 함수
register = template.Library()

@register.filter
def time_since(value):
    now = datetime.now()
    if value > now:
        return "미래"
    diff = now - value
    if diff.days > 0:
        return f"{diff.days}일 전"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}시간 전"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}분 전"
    else:
        return "방금 전"
