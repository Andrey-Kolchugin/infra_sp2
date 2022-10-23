from django.core.exceptions import ValidationError


def username_value_not_me(value):
    if value == 'me':
        raise ValidationError(
            'choose a different username',
            params={'value': value},
        )
