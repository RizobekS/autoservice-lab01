from django_cleanup.signals import cleanup_pre_delete

from apps.cars.utils.thumbnails import delete_old_thumbnails


# TODO: Check whether old images deletion works properly in production
def old_delete(file, **kwargs):
    delete_old_thumbnails(file, True)


cleanup_pre_delete.connect(old_delete)
