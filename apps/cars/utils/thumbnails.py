import os

from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from easy_thumbnails.models import Source, Thumbnail


def delete_old_thumbnails(image_field: ImageFieldFile, delete_source=False):
    if image_field:
        sources = Source.objects.filter(name=image_field.name)
        if sources.exists():
            success = 0
            thumbnails = Thumbnail.objects.filter(source=sources[0])
            for thumb in thumbnails:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, thumb.name))
                    thumb.delete()
                    success += 1
                except Exception as error:
                    print(f'{image_field}: Could not remove thumbnail {thumb}')
                    print(f'{error}, e.message')
                print(f'{image_field}: Deleted {success}/{thumbnails.count()} old thumbnail files')
            if delete_source:  # Delete source model (not file)
                for source in sources:
                    source.delete()
        image_field.close()
