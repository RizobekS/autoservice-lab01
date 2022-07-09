from collections import OrderedDict
from threading import Lock

from django.core.cache.backends.base import BaseCache
from django.core.cache.backends.locmem import LocMemCache


class RequestCache(LocMemCache):
    """
    RequestCache is a customized LocMemCache which stores its data cache as an instance attribute, rather than
    a global. It's designed to live only as long as the request object that RequestCacheMiddleware attaches it to.
    """

    def __init__(self):
        # We explicitly do not call super() here, because while we want BaseCache.__init__() to run, we *don't*
        # want LocMemCache.__init__() to run, because that would store our caches in its globals.
        BaseCache.__init__(self, {})

        self._cache = OrderedDict()
        self._expire_info = {}
        self._lock = Lock()


def RequestCacheMiddleware(get_response: callable):
    """
    Creates a fresh cache instance as request.cache. The cache instance lives only as long as request does.
    """

    def middleware(request):
        request.cache = RequestCache()

        response = get_response(request)

        return response

    return middleware
