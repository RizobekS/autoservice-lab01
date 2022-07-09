from django.db.models import Prefetch

from apps.cars.models import CarFilter
from apps.services.models import Section
from apps.site_settings.models import StaticInformation, Branch, MenuServiceSorting
from utils.car_filter import get_car_filter


def static_info(request):
    context = {item.key: item.value for item in StaticInformation.objects.filter(add_to_context=True)}
    context['navbar_branches'] = list(Branch.objects.filter(active=True).order_by('-id'))

    if request.user.is_authenticated:
        query_set = CarFilter.objects.select_related('vendor', 'model__vendor', 'year__model__vendor', 'modification__year__model__vendor').filter(user=request.user)
        context['garage_cars'] = query_set
    else:
        car_filter = get_car_filter(request)
        context['garage_cars'] = [car_filter] if car_filter else []
    context['garage_cars_count'] = len(context['garage_cars'])

    return context


def menu_data(request):
    queryset = MenuServiceSorting.objects.select_related('product', 'section')
    root_sections = Section.objects.prefetch_related(
        Prefetch('menuservicesorting_set', queryset=queryset.filter(active=True), to_attr='active_menusortingset')
    ).filter(active=True, parent_section=None)

    objects = {}
    for root_sec in root_sections:
        queryset = root_sec.active_menusortingset
        objects[root_sec] = [item.instance for item in queryset if item.instance.active]
    return {'menu_services': objects}
