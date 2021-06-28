from django.shortcuts import render

# Create your views here.
from apps.cars.models import Vendor
from apps.services.models import Section, Product


def index(request):
    vendors = Vendor.objects.filter(active=True)

    homepage_services = list(Section.objects.filter(active=True)) + list(Product.objects.filter(active=True))

    context = {
        'vendors': vendors,
        'homepage_services': homepage_services
    }

    return render(request, 'home/index.html', context=context)
