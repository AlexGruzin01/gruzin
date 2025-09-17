import datetime
from django.utils import timezone

from django import template
from myblog.models import *

register = template.Library()


# @register.inclusion_tag('alfablog/info.html')
# def show_info():
#     info = BlogInfo.objects.all()
#     return {'info': info}


# @register.inclusion_tag('myblog/cat.html')
# def show_cat():
#     category = Category.objects.all()
#     return {'category': category}

@register.simple_tag()
def get_category():
    return Category.objects.prefetch_related('posts')


@register.simple_tag()
def get_info():
    return Site.objects.all()


@register.simple_tag
def get_work_status():
    """
    Возвращает статус и соответствующий CSS-класс
    с учетом текущего времени, рабочих часов и дней недели.
    """
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    current_day = now.weekday()  # 0 - понедельник, 6 - воскресенье

    # Время работы
    opening_time = datetime.time(9, 0)  # Открывается в 9:00
    closing_time = datetime.time(17, 0)  # Закрывается в 17:00

    # Определяем рабочие дни (0-4 = пн-пт)
    is_work_day = current_day <= 4  # Понедельник - Пятница

    if not is_work_day:
        # Выходной день (суббота или воскресенье)
        return {'status': 'Выходной', 'class': 'status-closed'}

    # Проверяем рабочее время в рабочий день
    if opening_time <= closing_time:
        is_open = opening_time <= current_time <= closing_time
    else:
        # Для круглосуточных или ночных заведений
        is_open = current_time >= opening_time or current_time <= closing_time

    if is_open:
        return {'status': 'Открыто', 'class': 'status-open'}
    else:
        return {'status': 'Закрыто', 'class': 'status-closed'}