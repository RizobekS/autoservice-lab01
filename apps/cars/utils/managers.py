from django.db import models
from django.utils import timezone


class LastAccessedQuerySet(models.QuerySet):
    """
        Updates value of last_used field each time object is accessed
    """

    @staticmethod
    def _update_access_time(obj):  # Update do not update field more
        diff = timezone.now() - obj.last_used
        if obj and diff.seconds > 3:
            obj.save(update_fields=('last_used',))
        return obj

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        self._update_access_time(result)
        return result

    def first(self):
        result = super().first()
        self._update_access_time(result)
        return result

    def last(self):
        result = super().last()
        self._update_access_time(result)
        return result


class LastAccessedManager(models.Manager):
    def get_queryset(self):
        return LastAccessedQuerySet(self.model, using=self._db)
