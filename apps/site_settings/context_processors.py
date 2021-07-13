from apps.cars.models import CarFilter
from apps.services.models import Section
from apps.site_settings.models import StaticInformation, Branch
from utils.car_filter import get_car_filter


def static_info(request):
    context = {item.key: item.value for item in StaticInformation.objects.filter(add_to_context=True)}
    context['navbar_branches'] = Branch.objects.filter(active=True).order_by('-id')

    if request.user.is_authenticated:
        query_set = CarFilter.objects.filter(user=request.user)
        context['garage_cars'] = query_set
    else:
        car_filter = get_car_filter(request)
        context['garage_cars'] = [car_filter] if car_filter else []
    context['garage_cars_count'] = len(context['garage_cars'])

    return context


def menu_data(request):
    return {'menu_root_sections': Section.objects.filter(active=True, parent_section=None).order_by('id')}
