from marshmallow.exceptions import ValidationError


def validate_integer(value, *, min_value=None, max_value=None, choices=None):
    if min_value is not None:
        if value < min_value:
            raise ValidationError(
                f'Must be greater than or equal to {min_value}.'
            )

    if max_value is not None:
        if value > max_value:
            raise ValidationError(
                f'Must be less than or equal to {max_value}.'
            )

    if choices is not None:
        if value not in choices:
            raise ValidationError(
                f'Must be one of: {", ".join(map(repr, choices))}.'
            )


def validate_string(value, *, max_length=None, choices=None):
    if value == '':
        raise ValidationError('Field may not be blank.')

    if max_length is not None:
        if len(value) > max_length:
            raise ValidationError(
                f'Must be at most {max_length} characters long.'
            )

    if choices is not None:
        if value not in choices:
            raise ValidationError(
                f'Must be one of: {", ".join(map(repr, choices))}.'
            )
