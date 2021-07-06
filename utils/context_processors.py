from apps.services.models import Product


def menu_data(request):
    products = list(Product.objects.filter(active=True))
    root_sections = {}
    for product in products:
        root = product.root_section()
        if root in root_sections:  # and len(root_sections[root]) <= 5
            root_sections[root].append(product)
        else:
            root_sections[root] = [product]

    return {'menu_root_sections': root_sections}
