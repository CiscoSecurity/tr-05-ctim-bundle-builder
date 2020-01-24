import datetime as dt

from marshmallow import fields

from ..entity import Entity


class EntityRefField(fields.String):
    default_error_messages = {
        'invalid': 'Not a valid string or a CTIM entity.',
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, Entity):
            value = value.id
        return super()._deserialize(value, attr, data, **kwargs)


class DateTimeField(fields.NaiveDateTime):
    """A UTC datetime string with the Z suffix."""

    def __init__(self, **kwargs):
        kwargs['format'] = 'iso8601'
        kwargs['timezone'] = dt.timezone.utc
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dt.datetime):
            value = value.isoformat()

        # Validate as a proper ISO-formatted string,
        # but don't convert to a DateTime object.
        datetime = super()._deserialize(value, attr, data, **kwargs)

        return datetime.isoformat(timespec='milliseconds') + 'Z'
