import datetime
from datetime import timedelta

from django import template
from django.utils import timezone

from utils.helpers import get_ending

register = template.Library()

MONTHS = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')


@register.filter
def time_delta(date: datetime.datetime):
    if not isinstance(date, datetime.datetime):
        raise ValueError(f'date must be instance of datetime.datetime, got {type(date)} instead')

    now = timezone.now()

    if now.year == date.year:
        if date > now - timedelta(days=1):
            hours = round((now - date).seconds / 3600)
            if hours == 0:
                return "менее часа назад"
            else:
                return get_ending(hours, ('час назад', 'часа назад', 'часов назад'))
        else:
            date_string = date.strftime("%d {}")
            return date_string.format(MONTHS[date.month - 1])
    else:
        date_string = date.strftime("%d {} %Y")
        return date_string.format(MONTHS[date.month - 1])


@register.filter
def date_delta(date: datetime.date):
    if not isinstance(date, datetime.date):
        raise ValueError(f'date must be instance of datetime.date, got {type(date)} instead')

    now = timezone.now()

    if now.year == date.year and now.month == date.month and abs(now.day - date.day) <= 1:
        day_delta = now.day - date.day
        if day_delta == -1:
            prefix = 'Завтра, '
        elif day_delta == 0:
            prefix = 'Сегодня, '
        else:
            prefix = 'Вчера, '
    else:
        prefix = ''

    date_string = date.strftime("%d {} %Y")
    return prefix + date_string.format(MONTHS[date.month - 1])
