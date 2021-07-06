from django.db import models


class LastAccessedQuerySet(models.QuerySet):
    """
        Updates value of last_used field each time object is accessed
    """

    @staticmethod
    def _update_access_time(obj):
        if obj:
            obj.save(update_fields=('last_used',))
        return obj

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        # print('My get() is used :D')
        self._update_access_time(result)
        return result

    def first(self):
        result = super().first()
        # print('My first() is used :D')
        self._update_access_time(result)
        return result

    def last(self):
        result = super().last()
        # print('My last() is used :D')
        self._update_access_time(result)
        return result


class LastAccessedManager(models.Manager):
    def get_queryset(self):
        return LastAccessedQuerySet(self.model, using=self._db)
