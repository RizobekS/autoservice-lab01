from typing import Union

from django.db.models.signals import post_save, post_delete

from apps.services.models import Product, Section
from apps.site_settings.models import MenuServiceSorting


def create_section_one_to_one(sender, instance: Section, **kwargs):
    if not instance.is_root():
        root_section = instance.root_section()
        MenuServiceSorting.objects.get_or_create(root_section=root_section, section=instance, product=None)


def create_product_one_to_one(sender, instance: Product, **kwargs):
    root_section = instance.root_section()
    MenuServiceSorting.objects.get_or_create(root_section=root_section, section=None, product=instance)


post_save.connect(create_section_one_to_one, sender=Section, dispatch_uid='create_section_one_to_one')
post_save.connect(create_product_one_to_one, sender=Product, dispatch_uid='create_product_one_to_one')
