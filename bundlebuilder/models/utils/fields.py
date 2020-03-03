import datetime as dt

from marshmallow import fields

from ..entity import Entity


class EntityField(fields.Field):
    default_error_messages = {'invalid': 'Not a valid CTIM {type}.'}

    def __init__(self, **kwargs):
        type_ = kwargs.pop('type', None)
        ref = kwargs.pop('ref', False)

        super().__init__(**kwargs)

        self.type = (
            type_
            if isinstance(type_, type) and issubclass(type_, Entity) else
            Entity
        )
        self.attr = 'id' if ref else 'json'

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, self.type):
            return getattr(value, self.attr)

        raise self.make_error('invalid', type=self.type.__name__)


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
