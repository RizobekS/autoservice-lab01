import io
from timeit import default_timer

import xlsxwriter

from apps.cars.models import Modification


def export_cars() -> bytes:
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    sheet = workbook.add_worksheet('Активные машины')

    format_ = workbook.add_format()
    format_.set_align('center')

    sheet.set_column('A:A', 10, cell_format=format_)
    sheet.set_column('B:B', 30, cell_format=format_)
    sheet.set_column('C:C', 10, cell_format=format_)
    sheet.set_column('D:D', 80, cell_format=format_)

    headers = ('Марка', 'Модель', 'Год', 'Модификация')
    modifications = Modification.objects.select_related('year__model__vendor').filter(year__model__active=True, year__model__vendor__active=True)

    data = [(modification.year.model.vendor.name, modification.year.model.name, modification.year.year, modification.name) for modification in modifications]

    sheet.add_table(f'A1:D{len(data) + 1}', {'data': data, 'columns': [{'header': item} for item in headers]})

    workbook.close()

    return output.getvalue()
