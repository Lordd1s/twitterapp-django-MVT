import datetime
from django import template

register = template.Library()


@register.filter(name="format_datetime")
def format_datetime(source: datetime.datetime, format: str = ""):  # SIMPLE TAG
    """Преобразует дату в строку в формате datetime"""

    # , tz_hours: float = 6.0
    # source = source + datetime.timedelta(hours=tz_hours)

    match format:  # match-case (switch-case - js/go) - хэширует(запоминает) значения своих кейсов
        case "time":
            return source.strftime("%H:%M:%S")
        case "time1":
            return source.strftime("%H-%M-%S")
        case "date":
            return source.strftime("%d.%m.%Y")
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
