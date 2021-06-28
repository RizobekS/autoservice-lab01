from utils.helpers import admin_example

DESCRIPTION_HELP_TEXT = f'''
Примеры размещения: - для корневого раздела: {admin_example("description--root-section.png")}   - для НЕ корневого раздела: {admin_example("description--section.png")}
'''

TITLE_DATIVE_HELP_TEXT = f'''
Используется при выведении надписей типа "Другие работы по <b>ремонту двигателя</b>" или "Услуги по <b>ремонту двигателя</b>"
'''

ACTIVE_HELP_TEXT = f'''
Неактивные элементы не отображаются нигде кроме админ панели. Уберите галочку в этом поле, вместо удаления
'''

VENDOR_PAGE_THUMBNAIL_HELP_TEXT = f'''
Примеры размещения: {admin_example("vendor_page_thumbnail.png")}
'''
