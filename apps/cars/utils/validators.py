from django.core.exceptions import ValidationError


def validate_double_slash_url(value: str):
    if '--' in value:
        raise ValidationError(
            f'Url {value} must not contain double slash ("--")',
            params={'value': value}
        )
