from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.cars.models import Vendor


class CarsSitemap(Sitemap):
    def items(self):
        urls = []

        for vendor in Vendor.objects.filter(active=True):
            urls.append([vendor.url])

            for model in vendor.active_model_set():
                urls.append((vendor.url, model.url))

                for year in model.active_year_set():
                    for modification in year.active_modification_set():
                        urls.append((vendor.url, model.url, str(year.year), str(modification.id)))
        return urls

    def location(self, item):
        return reverse('cars:car', args=(item,))
