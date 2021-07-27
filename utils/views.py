from abc import abstractmethod

from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView

from utils.mixins import PageSettingsMixin


class StaticPageView(TemplateView, PageSettingsMixin):
    """
        Provides nice wrapper for pages with static content and configurable title and meta tags
    """


class FormDetailView(ProcessFormView):
    """
        Original DetailView do assign value for self.object ONLY when GET request is made
        This view extends this behaviour to POST and PUT request methods

        Class, inheriting from FormDetailView MUST IMPLEMENT get_object() method

        If it does not work as expected, try to change it's chain of parent classes.
        It must come before parent class, that uses self.object.
    """
    object = None

    @abstractmethod
    def get_object(self):
        raise NotImplementedError('get_object() method must be implemented')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def put(self, *args, **kwargs):
        self.object = self.get_object()
        return super().put(*args, **kwargs)
