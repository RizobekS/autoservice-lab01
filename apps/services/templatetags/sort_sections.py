from django import template

register = template.Library()


@register.filter
def sort_by_level(results):
    level_sections = {}
    for result in results:
        level = result.form.instance.level()
        if level in level_sections:
            level_sections[level].append(result)
        else:
            level_sections[level] = [result]

    return dict(sorted(level_sections.items())).items()
