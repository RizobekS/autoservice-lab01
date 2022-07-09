from typing import Optional

from apps.cars.models import CarFilter


def get_car_filter(request) -> Optional[CarFilter]:
    """
        Returns CarFilter object saved in session if it exists
        Or returns latest object from carfilter_set if user is authenticated
        None otherwise
    """
    filter_id = request.session.get(_FILTER_HASH, None)

    # Store car_filter in per request caches for furtuher calls
    car_filter = request.cache.get('car_filter', False)  # False if not in cache
    if car_filter is False:
        queryset = CarFilter.objects.select_related('vendor', 'model__vendor', 'year__model__vendor', 'modification__year__model__vendor').filter(id=filter_id)
        car_filter = queryset.first()
        request.cache.set('car_filter', car_filter)

    return car_filter


def set_car_filter(request, filter_obj: CarFilter) -> None:
    """
        Deletes previous CarFilter object if it exists and NOT bound to user,
        sets the new one and returns it back
    """
    if _FILTER_HASH in request.session:
        CarFilter.objects.filter(id=request.session[_FILTER_HASH], user=None).delete()
    if request.user.is_authenticated and filter_obj.is_full():
        filter_obj.user = request.user
        filter_obj.save()
    request.cache.set('car_filter', filter_obj)
    request.session[_FILTER_HASH] = filter_obj.id


def remove_car_filter(request, delete=True):
    """
        Removes _FILTER_HASH from session and deletes current CarFilter object if it exists
        Note: it deletes previous CarFilter object ONLY if it has no user specified
    """
    if _FILTER_HASH in request.session:
        if delete:
            CarFilter.objects.filter(id=request.session[_FILTER_HASH], user=None).delete()
        del request.session[_FILTER_HASH]
        request.cache.set('car_filter', False)


_FILTER_HASH = 'car_filter'
