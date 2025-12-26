from django import template

register = template.Library()

@register.filter
def make_list(time_obj, day_id):
    """
    Убакытты жана күндү кортежге бириктирет.
    Колдонулушу: {{ time|make_list:day }}
    """
    return (time_obj, day_id)

@register.filter
def get_lesson(full_schedule, key):
    """
    Сөздүктөн ачкыч боюнча сабакты табат.
    """
    if full_schedule:
        return full_schedule.get(key)
    return None