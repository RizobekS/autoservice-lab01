import re
import os
from gettext import ngettext

from django.contrib import admin, messages
from django.core.files.base import ContentFile
from django.db.models import QuerySet, ManyToManyField, FileField
from django.db.models.fields.files import FieldFile


def _clone_suffix(string: str) -> str:
    if re.search(r'__copy-\d$', string) is not None:
        current_n = re.search(r'\d$', string).group(0)
        string = re.sub(r'\d$', str(int(current_n) + 1), string)
    else:
        string = string + '__copy-1'
    return string


@admin.action(description='Дублировать')
def clone(modeladmin: admin.ModelAdmin, request, queryset: QuerySet):
    """
        This function is designed to be an admin action to clone each selected object

        Warning!
        This function isn't ideal, it has list of assumptions that may not suit you:
            - it assumes that each pk field is auto incremented (it sets pk field value to None)
            - it assumes that each unique field is textual (except pk fields)
    """

    unique_fieldnames = []
    m2m_fieldnames = []
    file_fieldnames = []
    fields = queryset.model._meta.get_fields()
    pk_fieldname = queryset.model._meta.pk.name
    for field in fields:
        if hasattr(field, 'unique') and getattr(field, 'unique') and field.name != pk_fieldname:
            unique_fieldnames.append(field.name)
        if isinstance(field, ManyToManyField):
            m2m_fieldnames.append(field.name)
        elif isinstance(field, FileField):
            file_fieldnames.append(field.name)

    for obj in queryset.reverse():
        # Retrieve objects from m2m relations
        m2m_field_values = {}
        for fieldname in m2m_fieldnames:
            m2m_field_values[fieldname] = getattr(obj, fieldname).all()

        # Clear PK
        setattr(obj, pk_fieldname, None)

        # Copy files
        for fieldname in file_fieldnames:
            file: FieldFile = getattr(obj, fieldname)
            split_filename = os.path.splitext(os.path.split(file.name)[1])
            new_file = ContentFile(file.read())
            new_file.name = _clone_suffix(split_filename[0]) + split_filename[1]
            setattr(obj, fieldname, new_file)

        # Update unique fields to prevent database from failing
        for fieldname in unique_fieldnames:
            string: str = getattr(obj, fieldname)
            if string is not None:
                string = _clone_suffix(string)
            setattr(obj, fieldname, string)

        # Save changes and generate new PK value
        obj.save()

        # Bring m2m relations back
        for fieldname, values in m2m_field_values.items():
            attr = getattr(obj, fieldname)
            attr.add(*values)


@admin.display(description='Активировать')
def activate(modelform, request, queryset):
    updated = queryset.update(active=True)
    messages.success(request, ngettext('%d акция была успешно активирована.', '%d акции были успешно активированы.', updated) % updated)


@admin.display(description='Деактивировать')
def deactivate(modelform, request, queryset):
    updated = queryset.update(active=False)
    messages.success(request, ngettext('%d акция была успешно деактивирована.', '%d акции были успешно деактивированы.', updated) % updated)
