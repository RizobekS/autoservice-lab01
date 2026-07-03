from typing import List, Set

from django.views.generic import TemplateView
from transliterate import slugify

from apps.masters.models import Master
from apps.masters.utils.mixins import MastersMixin
from utils.mixins import PageSettingsMixin


class AboutMastersView(TemplateView, MastersMixin, PageSettingsMixin):
    template_name = 'masters/new_about.html'
    viewname = 'masters:about'

    @staticmethod
    def _extract_needed_positions(masters: List[Master]) -> Set[str]:
        positions = set()

        for item in masters:
            positions.update(item.positions.all())

        for item in masters:
            for pos in item.positions.all():
                pos.slug = slugify(pos.name)

        return positions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = self._extract_needed_positions(context['masters'])
        return context
