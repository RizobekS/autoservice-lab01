from typing import Any, Dict

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import DetailView, TemplateView

from apps.accounts.forms import BodyRepairAppointmentForm, BodyRepairAppointmentImageFormSet
from apps.accounts.utils.mixins import ShortAppointmentMixin
from apps.promotions.models import Promotion, Category
from apps.promotions.utils.mixins import PromotionsMixin
from utils.breadcrumbs.types import Breadcrumb
from utils.breadcrumbs.utils import reverse_bc
from utils.mixins import PageSettingsMixin
from utils.opengraph import OpengraphMixin
from utils.opengraph.utils import og_thumbnail
from utils.views import FormDetailView


class PromotionListView(TemplateView, PromotionsMixin, PageSettingsMixin):
    template_name = 'promotions/promotions.html'
    viewname = 'promotions:list'


class PromotionCategoryView(DetailView, PromotionsMixin, PageSettingsMixin):
    template_name = 'promotions/promotions.html'
    viewname = 'promotions:category'
    initial_breadcrumbs = [reverse_bc(view=PromotionListView)]

    model = Category
    slug_field = 'url'
    slug_url_kwarg = 'category_url'

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.name, '#')]

    def get_promotions_queryset(self):
        queryset = super().get_promotions_queryset()
        return queryset.filter(category__url__exact=self.object.url)

    def get_ceo_context(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({'category': self.object.name})
        return super().get_ceo_context(**kwargs)


class PromotionView(DetailView, FormDetailView, PromotionsMixin, PageSettingsMixin, ShortAppointmentMixin, OpengraphMixin):
    # DetailView
    template_name = 'promotions/promotion.html'
    queryset = Promotion.objects.select_related('category').filter(active=True)
    slug_field = 'url'
    slug_url_kwarg = 'promotion_url'
    context_object_name = 'promotion'
    object: Promotion = None  # for typehints

    # PromotionsMixin
    promotions_max = 5
    promotions_context_name = 'other_promotions'

    # PageSettingsMixin
    viewname = 'promotions:promotion'
    initial_breadcrumbs = [reverse_bc(PromotionListView)]

    def get_object(self, queryset=None):
        if self.object is None:
            self.object = super().get_object(queryset)

        return self.object

    def get_og_tags(self, **kwargs) -> dict:
        meta_context = super().as_context()

        kwargs.update({
            'og:title': meta_context['page_title'],
            'og:description': meta_context['meta_description'],
            **og_thumbnail(self.request, self.object, 'icon_thumbnail'),
            'og:url': self.request.build_absolute_uri(self.request.path),
        })
        return super().get_og_tags(**kwargs)

    def get_current_breadcrumb(self):
        return [Breadcrumb(self.object.title, reverse('promotions:promotion', args=(self.object.url,)))]

    def get_ceo_context(self, **kwargs) -> Dict[str, Any]:
        obj = self.get_object()
        kwargs.update({'promotion': obj.title, 'short_description': strip_tags(obj.short_description)})
        return super().get_ceo_context(**kwargs)

    def get_ceo_template(self, ceo_object, field_name):
        """ Override default behaviour to support individual or category specific ceo values """
        # Custom fields with ceo values are the same, but has 'meta_' prefix
        text = getattr(self.object, f'meta_{field_name}', None)
        if text:  # Return individual value, if exists
            return text
        text = getattr(self.object.category, f'meta_{field_name}', None)
        if text:  # If individual value is not specified, try category mask
            return text
        else:  # If neither category mask nor promotion specific values are not specified, use default one
            return super().get_ceo_template(ceo_object, field_name)

    # PromotionsMixin
    def get_promotions_queryset(self):
        return super().get_promotions_queryset().exclude(id=self.object.id)

    def get_context_data(self, **kwargs):
        return super().get_context_data(categories=Category.objects.all(), **kwargs)


class BodyRepairAppointmentView(View, PageSettingsMixin):
    template_name = 'services/spare_parts.html'

    def get(self, request):
        form = BodyRepairAppointmentForm()
        formset = BodyRepairAppointmentImageFormSet()

        context = {
            'form': form,
            'formset': formset
        }

        return render(request, 'promotions/body_repair_appointment.html', context=context)

    def post(self, request, *args, **kwargs):
        form = BodyRepairAppointmentForm(request.POST.copy())
        if form.is_valid():
            appointment = form.save()
            formset = BodyRepairAppointmentImageFormSet(request.POST.copy(), request.FILES.copy(), instance=appointment)

            if formset.is_valid():
                formset.save()
                form.send_mail(self.request)
                form.send_calltouch_request(self.request)
                messages.success(self.request, 'Заявка была успешно отправлена ✔', extra_tags='text-success')
                return redirect('promotions:body-repair-appointment')
            else:
                form = BodyRepairAppointmentForm(request.POST, request.FILES)
                formset = BodyRepairAppointmentImageFormSet(request.POST, request.FILES)
        else:
            formset = BodyRepairAppointmentImageFormSet(request.POST, request.FILES)

        return render(request, 'promotions/body_repair_appointment.html', {'form': form, 'formset': formset})
