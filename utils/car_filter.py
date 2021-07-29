from typing import Optional

from django.http import HttpRequest

from apps.cars.models import CarFilter


def get_car_filter(request: HttpRequest) -> Optional[CarFilter]:
    """
        Returns CarFilter object saved in session if it exists
        Or returns latest object from carfilter_set if user is authenticated
        None otherwise
    """
    filter_id = request.session.get(_FILTER_HASH, None)
    car_filter = CarFilter.objects.filter(id=filter_id)
    if car_filter.exists():
        return car_filter.first()

def set_car_filter(request: HttpRequest, filter_obj: CarFilter) -> None:
    """
        Deletes previous CarFilter object if it exists and NOT bound to user,
        sets the new one and returns it back
    """
    if _FILTER_HASH in request.session:
        CarFilter.objects.filter(id=request.session[_FILTER_HASH], user=None).delete()
    if request.user.is_authenticated and filter_obj.is_full():
        filter_obj.user = request.user
        filter_obj.save()
    request.session[_FILTER_HASH] = filter_obj.id


def remove_car_filter(request: HttpRequest, delete=True):
    """
        Removes _FILTER_HASH from session and deletes current CarFilter object if it exists
        Note: it deletes previous CarFilter object ONLY if it has no user specified
    """
    if _FILTER_HASH in request.session:
        if delete:
            CarFilter.objects.filter(id=request.session[_FILTER_HASH], user=None).delete()
        del request.session[_FILTER_HASH]


_FILTER_HASH = 'car_filter'
