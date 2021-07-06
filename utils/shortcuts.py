from typing import Union

from django.forms import BaseForm
from django.http import Http404


def exists_or_404(query_set, message: str = None):
    if query_set.exists():
        return query_set.first()
    else:
        raise Http404(message)


def add_attrs(obj: BaseForm, placeholders: dict = None, classes: Union[dict, str] = None):
    """
        Recommended to be called from __init__ of your form after call to super().__init__
        Populates your form field placeholders and/or classes with data passed as arguments.

        Example of either classes or placeholders attribute:
        PLACEHOLDERS = {
            'my_field': 'My placeholder for my_field',
        }

        If classes passed as string, these classes will be concatenated to all fields
        Note: new classes are concatenated to the old ones, while placeholders are replaced
    """

    fields = obj.fields

    if placeholders:
        if not isinstance(placeholders, dict):
            raise ValueError('placeholders argument must be of dict type. See method definition.')
        for key, placeholder in placeholders.items():
            fields[key].widget.attrs['placeholder'] = placeholder
    if classes:
        if isinstance(classes, dict):
            for key, class_ in classes.items():
                fields[key].widget.attrs['class'] = f'{fields[key].widget.attrs["class"]} {class_}' if 'class' in fields[key].widget.attrs else class_
        elif isinstance(classes, str):
            for item in fields:
                fields[item].widget.attrs['class'] = f'{fields[item].widget.attrs["class"]} {classes}' if 'class' in fields[item].widget.attrs else classes
        else:
            raise ValueError('classes argument must be of dict type. See method definition.')
