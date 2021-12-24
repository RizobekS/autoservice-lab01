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


def og_thumbnail(request, instance, thumbnail_field: str) -> dict:
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
    :param thumbnail_field: Name of thumbnail field
    :return: Dictionary, containing all needed values
    """

    from image_cropping.templatetags.cropping import cropped_thumbnail

    ratio_field = instance._meta.get_field(thumbnail_field)

    thumbnail_url = cropped_thumbnail(None, instance, thumbnail_field)

    data = {'og:image': request.build_absolute_uri(thumbnail_url),
            'og:image:width': ratio_field.width,
            'og:image:height': ratio_field.height}
    return data
