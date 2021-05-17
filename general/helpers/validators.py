from django.core.exceptions import ValidationError

def validate_year(value):
    if value < 1900 or value > 2100:
        raise ValidationError(
            '%(value)s is not a valid year(1900 - 2100)',
            params={'value': value},
        )