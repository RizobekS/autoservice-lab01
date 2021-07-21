from django.views.generic import TemplateView

from utils.mixins import PageSettingsMixin


class StaticPageView(TemplateView, PageSettingsMixin):
    """
        Provides nice wrapper for pages with static content and configurable title and meta tags
    """
