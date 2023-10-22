import datetime
from django import template

register = template.Library()


@register.filter(name="format_datetime")
def format_datetime(source: datetime.datetime, format: str = ""): 
    """Преобразует дату в строку в формате datetime"""

    match format:  
        case "time":
            return source.strftime("%H:%M:%S")
        case "time1":
            return source.strftime("%H-%M-%S")
        case "date":
            return source.strftime("%d.%m.%Y %H:%M")
        case "date2":
            return source.strftime("%d/%m/%Y")
        case _:
            return source


@register.filter(name="digit_beautify")
def digit_beautify(number):
    number_str = str(number)
    groups = []
    for i in range(0, len(number_str), 3):
        groups.append(number_str[i : i + 3])

    beautified = " ".join(groups[::-1])
    return beautified
