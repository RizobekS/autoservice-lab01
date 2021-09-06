from typing import List

from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from image_cropping.templatetags.cropping import cropped_thumbnail

from apps.cars.utils.mixins import CarFilterPageSettingsMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.mixins import PageSettingsMixin
from utils.views import FormDetailView
from .models import Section, Product
from .utils.helpers import service_url
from .utils.mixins import ProductsMixin, SectionsMixin, SingleSectionMixin
from ..accounts.utils.mixins import ShortAppointmentMixin, SparePartAppointmentMixin
from ..site_settings.models import StaticInformation


class SectionView(DetailView, SectionsMixin, ProductsMixin, CarFilterPageSettingsMixin):
    # #### DetailView ####
    template_name = 'services/section.html'
    queryset = Section.objects.filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'section_url'
    context_object_name = 'current_section'
    object: Section = None  # for typehints

    # #### SectionsMixin and ProductsMixin ####

    sections_context_name = 'child_sections'
    products_context_name = 'child_products'

    def get_sections_queryset(self):
        return Section.objects.filter(parent_section=self.object)

    def get_products_queryset(self):
        return Product.objects.filter(section=self.object)

    # #### CarFilterPageSettingsMixin ####

    viewname = 'services:section'
    viewname_suffix = '_car'

    def get_initial_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = []
        section = self.object.parent_section
        while section:
            breadcrumbs.append(Breadcrumb(section.title, service_url(self.request, section, True)))
            section = section.parent_section
        return breadcrumbs[::-1]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, service_url(self.request, self.object, True))]

    def get_ceo_context(self):
        context = super().get_ceo_context()
        context['section'] = self.object.title
        return context

    def get_ceo_template(self, ceo_object, field_name):
        """ Override default behaviour to support individual ceo values """
        # Custom fields with ceo values are the same, but has 'meta_' prefix
        text = getattr(self.object, f'meta_{field_name}', None)
        if text:  # Return individual value, if exists
            return text
        else:  # If not, use default one
            return super().get_ceo_template(ceo_object, field_name)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'image_url': cropped_thumbnail(None, self.object, 'thumbnail_1960x600'),
            'image_alt': self.object.title,
        })
        return super().get_context_data(**kwargs)


class ProductView(DetailView, FormDetailView, SingleSectionMixin, ProductsMixin, CarFilterPageSettingsMixin, ShortAppointmentMixin):
    # #### DetailView ####
    template_name = 'services/product.html'
    queryset = Product.objects.filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'product_url'
    context_object_name = 'product'
    object: Product = None  # for typehints

    # #### SingleSectionMixin ####
    def get_current_section(self):
        return self.object.section

    # #### ProductsMixin ####

    products_context_name = 'other_products'

    def get_products_queryset(self):
        return Product.objects.filter(section_id=self.object.section.id).exclude(id=self.object.id)

    # #### CarFilterPageSettingsMixin ####

    viewname = 'services:product'
    viewname_suffix = '_car'

    def get_initial_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = []
        section = self.object.section
        while section:
            breadcrumbs.append(Breadcrumb(section.title, service_url(self.request, section, True)))
            section = section.parent_section
        return breadcrumbs[::-1]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, service_url(self.request, self.object, True))]

    def get_ceo_context(self):
        context = super().get_ceo_context()
        context.update({
            'section': self.object.section.title,
            'product': self.object.title
        })
        return context

    def get_ceo_template(self, ceo_object, field_name):
        """ Override default behaviour to support individual ceo values """
        # Custom fields with ceo values are the same, but has 'meta_' prefix
        text = getattr(self.object, f'meta_{field_name}', None)
        if text:  # Return individual value, if exists
            return text
        else:  # If not, use default one
            return super().get_ceo_template(ceo_object, field_name)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'image_url': cropped_thumbnail(None, self.object, 'thumbnail_1960x600'),
            'image_alt': self.object.title,
            'happy_clients': StaticInformation.objects.get(key='advantages__happy_clients').value,
            'orders': StaticInformation.objects.get(key='advantages__orders').value,
            'positive_reviews': StaticInformation.objects.get(key='advantages__positive_reviews').value,
        })
        if self.object.canonical_to_original:
            kwargs['canonical_link'] = self.request.build_absolute_uri(reverse('services:product', kwargs={'product_url': self.object.url}))
        return super().get_context_data(**kwargs)

    # Check whether product suits the product
    # def get(self, *args, **kwargs):
    #     self.car_filter = self.get_car_filter()
    #     self.object = self.get_object()
    #
    #     if self.car_filter.modification.id in self.object.cars:
    #         return super().get(*args, **kwargs)
    #     else:
    #         return redirect() TODO: redirect to page incompatible.html


class SparePartsView(TemplateView, SparePartAppointmentMixin, PageSettingsMixin):
    template_name = 'services/spare_parts.html'
    viewname = 'services:spare_parts'
