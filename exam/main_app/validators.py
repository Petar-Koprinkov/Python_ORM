from django.core.exceptions import ValidationError


def digits_validator(value):
    for char in value:
        if not char.isdigit():
            raise ValidationError('Must contain only digits')