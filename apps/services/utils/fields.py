from timeit import default_timer

from django import forms
from django.db import models
from django.forms.models import ModelChoiceIterator

from apps.cars.models import Modification


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
        that is why OptimizedModelChoiceIterator exists (~6 seconds to retrieve all names) (Currently 0.19s, after adding additional full_name field)
    """
    def __iter__(self):
        start = default_timer()

        modification_set = Modification.objects.all()
        for modification in modification_set:
            yield modification.id, str(modification)
        print(f'\nOverall time: {default_timer() - start}s\n')


class OptimizedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
        Default ModelMultipleChoiceField is overridden to substitute OptimizedModelChoiceIterator instead of ModelChoiceIterator
    """
    iterator = OptimizedModelChoiceIterator
