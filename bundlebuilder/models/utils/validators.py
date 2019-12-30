from marshmallow import ValidationError, fields


def validate_datetime(value):
    # Validate as a proper ISO-formatted string,
    # but don't convert to a DateTime object.
    fields.DateTime().deserialize(value)


def validate_integer(value, *, min_value=None, max_value=None, choices=None):
    if min_value is not None:
        if value < min_value:
            raise ValidationError(
                'Must be greater than or equal to {}.'.format(min_value)
            )

    if max_value is not None:
        if value > max_value:
            raise ValidationError(
                'Must be less than or equal to {}.'.format(max_value)
            )

    if choices is not None:
        if value not in choices:
            raise ValidationError(
                'Must be one of: {}.'.format(
                    ', '.join(map(repr, choices))
                )
            )


def validate_string(value, *, max_length=None, choices=None):
    if value == '':
        raise ValidationError('Field may not be blank.')

    if max_length is not None:
        if len(value) > max_length:
            raise ValidationError(
                'Must be at most {} characters long.'.format(max_length)
            )

    if choices is not None:
        if value not in choices:
            raise ValidationError(
                'Must be one of: {}.'.format(
                    ', '.join(map(repr, choices))
                )
            )
