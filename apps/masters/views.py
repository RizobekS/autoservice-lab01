from django.views.generic import TemplateView

from apps.masters.utils.mixins import MastersMixin
from utils.mixins import PageSettingsMixin


class AboutMastersView(TemplateView, MastersMixin, PageSettingsMixin):
    template_name = 'masters/about.html'
    viewname = 'masters:about'
