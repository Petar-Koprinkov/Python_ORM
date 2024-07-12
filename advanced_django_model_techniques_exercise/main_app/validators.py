from django.core.exceptions import ValidationError


def name_validator(value):
    for char in value:
        if not (char.isspace() or char.isalpha()):
            raise ValidationError('Name can only contain letters and spaces')