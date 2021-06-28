from typing import Callable


class CarFilterUtilsMixin:
    vendor = None
    model = None
    year = None
    modification = None

    def existing_attributes(self) -> list:
        existing_attrs = []
        if self.vendor:
            existing_attrs.append(self.vendor)
            if self.model:
                existing_attrs.append(self.model)
                if self.year:
                    existing_attrs.append(self.year)
                    if self.modification:
                        existing_attrs.append(self.modification)
        return existing_attrs

    def full_name(self) -> str:
        return ' '.join([item.name for item in self.existing_attributes()])

    def url_args(self) -> tuple:
        last_existing_attr = self.existing_attributes()[-1]
        return last_existing_attr.url_args()
