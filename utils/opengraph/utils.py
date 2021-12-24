from apps.site_settings.models import StaticInformation


def og_full_title(title: str) -> dict:
    title_prefix_obj, title_suffix_obj = StaticInformation.objects.filter(key__in=('title_prefix', 'title_suffix'))
    return {'og:title': f'{title_prefix_obj.value} {title} {title_suffix_obj.value}'}


def og_image(request, image_field) -> dict:
    """
        Shortcut for getting needed thumbnail OpenGraph fields

        Just call this function like this:
        my_opengraph_data = {
            # Your keys and values
            my_key: my_value,
            **og_image(request, my_obj.image)
        }

    :param request: Request instance - used for building absolute url
    :param image_field:
    :return: Dictionary, containing all needed values
    """
    return {'og:image': request.build_absolute_uri(image_field.url),
            'og:image:width': image_field.width,
            'og:image:height': image_field.height}


def og_thumbnail(request, instance, thumbnail_field) -> dict:
    """
        Shortcut for getting needed thumbnail OpenGraph fields

        Just call this function like this:
        my_opengraph_data = {
            # Your keys and values
            my_key: my_value,
            **og_thumbnail(request, my_obj, 'my_thumbnail_field_name')
        }

    :param request: Request instance - used for building absolute url
    :param instance: Model instance, that contain thumbnail field
    :param thumbnail_field: Name of thumbnail field (image field automatically guessed through thumbnail field)
    :return: Dictionary, containing all needed values
    """

    from image_cropping.templatetags.cropping import cropped_thumbnail

    ratio_field = instance._meta.get_field(thumbnail_field)
    image_field = getattr(instance, ratio_field.image_field)  # get Imagefield

    thumbnail_url = cropped_thumbnail(None, instance, thumbnail_field)

    data = {'og:image': request.build_absolute_uri(thumbnail_url),
            'og:image:width': image_field.width,
            'og:image:height': image_field.height}
    return data


def og_current_url(request) -> dict:
    """
        Shortcut for rendering og:url OpenGraph field

        Just call this function like this:
        my_opengraph_data = {
            # Your keys and values
            my_key: my_value,
            **og_current_url(request),
        }

    :param request: Request instance - used for building absolute url
    :return: Dictionary, containing all needed values
    """
    return {'og:url': request.build_absolute_uri(request.path)}
