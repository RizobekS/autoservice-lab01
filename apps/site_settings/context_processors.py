import json

from django.db.models import Prefetch

from apps.cars.models import CarFilter
from apps.editor_pages.models import EditorPage
from apps.services.models import Section
from apps.site_settings.models import StaticInformation, Branch, MenuServiceSorting
from utils.car_filter import get_car_filter
from autoservice.settings.common import SMARTCAPTCHA_CLIENT_KEY


def static_info(request):
    context = {item.key: item.value for item in StaticInformation.objects.filter(add_to_context=True)}
    branches = list(Branch.objects.filter(active=True).order_by('-id'))
    context['navbar_branches'] = branches

    # NEW: map payload for pages that don't override it (home, contacts)
    payload = []
    for b in branches:
        if b.latitude is None or b.longitude is None:
            continue
        payload.append({
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "phone": b.phone,
            "lat": float(b.latitude),
            "lon": float(b.longitude),
        })
    context["map_branches_json"] = json.dumps(payload, ensure_ascii=False)

    if request.user.is_authenticated:
        query_set = CarFilter.objects.select_related('vendor', 'model__vendor', 'year__model__vendor', 'modification__year__model__vendor').filter(user=request.user)
        context['garage_cars'] = query_set
    else:
        car_filter = get_car_filter(request)
        context['garage_cars'] = [car_filter] if car_filter else []
    context['garage_cars_count'] = len(context['garage_cars'])

    context['footer_about'] = [(item.title, item.url)
                               for item in EditorPage.objects.filter(active=True, show_in_footer=EditorPage.FOOTER_ABOUT)]
    context['footer_additional_services'] = [(item.title, item.url)
                                             for item in EditorPage.objects.filter(active=True, show_in_footer=EditorPage.FOOTER_ADDITIONAL_SERVICES)]

    return context


def menu_data(request):
    queryset = MenuServiceSorting.objects.select_related('product', 'section')
    root_sections = Section.objects.prefetch_related(
        Prefetch('menuservicesorting_set', queryset=queryset.filter(active=True), to_attr='active_menusortingset')
    ).filter(active=True, parent_section=None)

    objects = {}
    for root_sec in root_sections:
        queryset = root_sec.active_menusortingset
        objects[root_sec] = [
            item.instance for item in queryset
            if item.instance.active and not getattr(item.instance, 'template_without_design', False)
        ]

    menu_editor_pages = [(item.title, item.url)
                         for item in EditorPage.objects.filter(active=True, show_in_menu=True)]

    return {'menu_services': objects,
            'menu_editor_pages': menu_editor_pages}

def smartcaptcha_keys(request):
    return {
        'SMARTCAPTCHA_CLIENT_KEY': SMARTCAPTCHA_CLIENT_KEY,
    }
