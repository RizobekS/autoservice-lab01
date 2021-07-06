from pathlib import Path
from typing import Any

from django.templatetags.static import static
from django.utils.safestring import mark_safe

ADMIN_EXAMPLES_ROOT = Path('images') / 'admin-examples'


def admin_example(image_name: str, name: str = 'Посмотреть'):
    link = static(str(ADMIN_EXAMPLES_ROOT / image_name))
    return link_tag(link, name, True, 'font-weight: bold; text-decoration: underline;')


def link_tag(link: str, name: Any = None, target_blank=False, style=''):
    target_blank = 'target="_blank"' if target_blank else ''
    style = f'style="{style}"' if style else style
    return f'<a {target_blank} href="{link}" {style}>{name if name else link}</a>'


def link_tag_safe(link: str, name: Any = None, target_blank=False, style=''):
    return mark_safe(link_tag(link=link, name=name, target_blank=target_blank, style=style))


def hidden_field_tag(name: str, url: str) -> str:
    return f'<input type="hidden" name="{name}" value="{url}"/>'


def format_price(number: float, currency: str = None) -> str:
    decimal, fractional = str(number).split('.')
    decimal = decimal[::-1]
    price = " ".join([decimal[i:i + 3] for i in range(0, len(decimal), 3)])[::-1]
    price = f'{price}.{fractional}' if fractional is not '0' else str(price)
    return f'{price}{currency}' if currency else price


def get_ending(number, options):
    if len(options) != 3:
        raise ValueError(f'3 options required, got {len(options)} instead')
    number = str(number)
    last_char = int(number[-1:])
    if last_char == 1 and number[-2:] != '11':
        return f"{number} {options[0]}"
    elif 2 <= last_char <= 4 and number[-2:] != "12" and number[-2:] != "13" and number[-2:] != "14":
        return f"{number} {options[1]}"
    else:
        return f"{number} {options[2]}"
