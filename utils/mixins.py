from apps.site_settings.utils.mixins import CEOMixin
from utils.breadcrumbs.mixins import BreadcrumbsMixin
from utils.breadcrumbs.types import Breadcrumb


class PageSettingsMixin(BreadcrumbsMixin, CEOMixin):
    """
        Combines BreadcrumbsMixin and CEOMixin

        viewname: str - view name for constructing reverse url
    """
    viewname: str = None

    def get_current_breadcrumb(self):
        if self.current_breadcrumb:
            return super().get_current_breadcrumb()
        else:
            return [Breadcrumb(self.get_page_title(), '#')]
