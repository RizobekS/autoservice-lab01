from timeit import default_timer

from django import forms
from django.db import models
from django.forms.models import ModelChoiceIterator

from apps.cars.models import Vendor, Model, Year, Modification


class OptimizedManyToManyField(models.ManyToManyField):
    """
        Default ManyToManyField is overridden to substitute OptimizedModelMultipleChoiceField instead of ModelMultipleChoiceField
    """

    def formfield(self, *, using=None, **kwargs):
        defaults = {
            'form_class': OptimizedModelMultipleChoiceField,
            **kwargs,
        }
        return super().formfield(**defaults)


class OptimizedModelChoiceIterator(ModelChoiceIterator):
    """
        Queryset lookup that ModelChoiceIterator performs is too slow in case of cars app (~24 seconds to retrieve all names),
        that is why OptimizedModelChoiceIterator exists (~6 seconds to retrieve all names)
    """

    def __iter__(self):
        start = default_timer()

        vendor_set = Vendor.objects.filter(active=True)
        for vendor in vendor_set:
            model_set = Model.objects.filter(vendor=vendor)
            vendor_name = vendor.name
            for model in model_set:
                year_set = Year.objects.filter(model=model)
                model_name = model.name
                for year in year_set:
                    modification_set = Modification.objects.filter(year=year)
                    year_name = year.name
                    for modification in modification_set:
                        yield modification.id, ' - '.join((vendor_name, model_name, year_name, modification.name))
        print(f'Overall time: {default_timer() - start}s')


class OptimizedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
        Default ModelMultipleChoiceField is overridden to substitute OptimizedModelChoiceIterator instead of ModelChoiceIterator
    """
    iterator = OptimizedModelChoiceIterator
