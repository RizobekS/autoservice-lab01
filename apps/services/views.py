from random import randint
from typing import List

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import DetailView, TemplateView
from image_cropping.templatetags.cropping import cropped_thumbnail

from apps.cars.utils.mixins import CarFilterPageSettingsMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.car_filter import get_car_filter
from utils.mixins import PageSettingsMixin
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_thumbnail, og_full_title
from utils.views import FormDetailView
from .models import Section, Product
from .utils.helpers import service_url
from .utils.mixins import ProductsMixin, SectionsMixin, SingleSectionMixin
from ..accounts.forms import CallRequestForm
from ..accounts.utils.mixins import ShortAppointmentMixin, SparePartAppointmentMixin
from ..news.models import Article
from ..promotions.models import Promotion
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
            if section.url != 'others':
                breadcrumbs.append(Breadcrumb(section.title, service_url(self.request, section, True)))
            section = section.parent_section
        return breadcrumbs[::-1]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, service_url(self.request, self.object, True))]

    def get_ceo_context(self, **kwargs):
        kwargs.update({
            'section': self.object.title,
            'short_description': strip_tags(self.object.short_description),
        })
        return super().get_ceo_context(**kwargs)

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
        if self.object.canonical_to_original:
            kwargs['canonical_link'] = self.request.build_absolute_uri(reverse('services:section', kwargs={'section_url': self.object.url}))
        return super().get_context_data(**kwargs)


class ProductView(DetailView, FormDetailView, SingleSectionMixin, CarFilterPageSettingsMixin, ShortAppointmentMixin, OpengraphMixin):
    # #### DetailView ####
    template_name = 'services/product.html'
    queryset = Product.objects.filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'product_url'
    context_object_name = 'product'

    def get_og_tags(self, **kwargs) -> dict:
        kwargs.update({
            **og_full_title(self.object.title),
            'og:description': self.object.short_description,
            **og_thumbnail(self.request, self.object, 'thumbnail_960x585'),
            'og:url': self.request.build_absolute_uri(reverse('services:product', kwargs={'product_url': self.object.url})),
        })
        return super().get_og_tags(**kwargs)

    def get_form(self, form_class=None):
        """
            Override branch choices to contain only supported branches.
            This function works both for ShortAppointmentForm and CallRequestForm (because both forms use the same choices field, I guess)
        """
        form_class = super().get_form(form_class)
        choices = [(item.id, item.name) for item in self.object.branches.get_queryset()]
        if len(choices) > 1:
            choices.insert(0, ('', 'Выберите СТО'))
        form_class.fields['branch'].choices = choices
        return form_class

    def dispatch(self, request, *args, **kwargs):
        self.object: Product = None  # for typehints
        self.car_filter = None
        return super().dispatch(request, *args, **kwargs)

    # #### SingleSectionMixin ####
    def get_current_section(self):
        return self.object.section

    # #### CarFilterPageSettingsMixin ####

    viewname = 'services:product'
    viewname_suffix = '_car'

    def get_initial_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = []
        section = self.object.section
        while section:
            if section.url != 'others':
                breadcrumbs.append(Breadcrumb(section.title, service_url(self.request, section, True)))
            section = section.parent_section
        return breadcrumbs[::-1]

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, service_url(self.request, self.object, True))]

    def get_ceo_context(self, **kwargs):
        kwargs.update({
            'section': self.object.section.title,
            'product': self.object.title,
            'short_description': strip_tags(self.object.short_description)
        })
        return super().get_ceo_context(**kwargs)

    def get_ceo_template(self, ceo_object, field_name):
        """ Override default behaviour to support individual ceo values """
        # Custom fields with ceo values are the same, but has 'meta_' prefix
        text = getattr(self.object, f'meta_{field_name}', None)
        if text:  # Return individual value, if exists
            return text
        else:  # If not, use default one
            return super().get_ceo_template(ceo_object, field_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'image_url': cropped_thumbnail(None, self.object, 'thumbnail_1960x600'),
            'image_alt': self.object.title,
            'happy_clients': StaticInformation.objects.get(key='advantages__happy_clients').value,
            'orders': StaticInformation.objects.get(key='advantages__orders').value,
            'positive_reviews': StaticInformation.objects.get(key='advantages__positive_reviews').value,
            'average_score': StaticInformation.objects.get(key='advantages__average_score').value,
            'call_request_form': CallRequestForm(self.request.POST) if self.request.method == 'post' else CallRequestForm(),
            'promotions': self.get_promotions(),
            'articles': self.get_articles(),
            'related_works': self.get_related_works(),
            'other_products': self.object.section.active_product_descendants({'id': self.object.id}),
        })
        if self.object.canonical_to_original:
            context['canonical_link'] = self.request.build_absolute_uri(reverse('services:product', kwargs={'product_url': self.object.url}))
        return context

    def get_promotions(self):
        """ Get related promotions (each promotion can be related to a product). If no related promotions - select 3 arbitrary ones """
        promotions = self.object.promotion_set.filter(active=True)
        if promotions.exists():
            promotions = promotions[:3]
        else:
            # Get random promotion entries
            queryset = Promotion.objects.filter(active=True)
            promotions = []
            count = queryset.count()
            min_count = min(3, count)  # In case if there are less than 3 Promotions
            while len(promotions) < min_count:
                rand = randint(0, count - 1)
                item = queryset[rand]
                if item not in promotions:
                    promotions.append(item)
        return promotions

    def get_articles(self):
        """ Get related articles (each article can be related to a product). If no related articles - select 3 arbitrary ones """
        articles = self.object.article_set.filter(is_news=False, status='published')
        if articles.exists():
            articles = articles[:3]
        else:
            # Get random article entries
            queryset = Article.objects.filter(is_news=False, status='published')
            articles = []
            count = queryset.count()
            min_count = min(4, count)  # In case if there is less than 4 articles
            while len(articles) < min_count:
                rand = randint(0, count - 1)
                item = queryset[rand]
                if item not in articles:
                    articles.append(item)
        return articles

    def get_related_works(self):
        """
            If no car_filter - all active works related to this product are retrieved
            if car_filter is present - only active works related to this product with the matching model
            if no model but only vendor in car_filter is present - only active works related to this product with the matching vendors (vendors are retrieved using models)
        """
        queryset = self.object.work_set.filter(active=True)
        car_filter = get_car_filter(self.request)
        if car_filter is not None and car_filter.model:
            works = queryset.filter(model_pack__models=car_filter.model).distinct()
        elif car_filter is not None and car_filter.vendor:
            works = queryset.filter(model_pack__models__vendor=car_filter.vendor).distinct()
        else:
            works = queryset.all()
        return works[:5]

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


class SubmitCallRequestView(View):

    def post(self, request):
        form = CallRequestForm(data=self.request.POST)
        if form.is_valid():
            obj = form.save()
            form.send_mail(request)
            messages.success(request, 'Заявка на звонок была успешно отправлена ✔', extra_tags='text-success')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
