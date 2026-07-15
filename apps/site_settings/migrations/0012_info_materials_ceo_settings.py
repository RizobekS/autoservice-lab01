from django.db import migrations


SETTINGS = (
    {
        'key': 'knowledge_base:blog',
        'page': 'Статьи',
        'title': 'Статьи',
        'header': 'Статьи',
        'description': 'Статьи автосервиса',
    },
    {
        'key': 'knowledge_base:faq',
        'page': 'Вопрос-ответ',
        'title': 'Вопрос-ответ',
        'header': 'Вопрос-ответ',
        'description': 'Ответы на вопросы по обслуживанию автомобилей',
    },
    {
        'key': 'knowledge_base:symptom-list',
        'page': 'Симптомы',
        'title': 'Симптомы',
        'header': 'Симптомы',
        'description': 'Симптомы неисправностей автомобиля',
    },
)


def create_ceo_settings(apps, schema_editor):
    CEOSetting = apps.get_model('site_settings', 'CEOSetting')
    for item in SETTINGS:
        CEOSetting.objects.get_or_create(
            key=item['key'],
            defaults={
                'page': item['page'],
                'title': item['title'],
                'header': item['header'],
                'description': item['description'],
                'keywords': '',
                'robots': '',
                'variables': '',
            },
        )


def delete_ceo_settings(apps, schema_editor):
    CEOSetting = apps.get_model('site_settings', 'CEOSetting')
    CEOSetting.objects.filter(key__in=[item['key'] for item in SETTINGS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('site_settings', '0011_auto_20260208_1927'),
    ]

    operations = [
        migrations.RunPython(create_ceo_settings, delete_ceo_settings),
    ]
