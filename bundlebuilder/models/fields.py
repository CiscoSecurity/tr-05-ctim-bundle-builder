import datetime as dt

from marshmallow import fields

from .entity import BaseEntity


class EntityField(fields.Field):
    default_error_messages = {
        'type': 'Not a valid CTIM {type_name}.',
        'attr': "Missing required attribute: '{attr_name}'.",
    }

    def __init__(self, **kwargs):
        self.type = kwargs.pop('type', BaseEntity)
        if not (
            isinstance(self.type, type) and issubclass(self.type, BaseEntity)
        ):
            raise ValueError(f"'type' must be a subclass of {BaseEntity}.")

        self.type_name = kwargs.pop('type_name', self.type.__name__)

        ref = kwargs.pop('ref', False)
        if not isinstance(ref, bool):
            raise ValueError(f"'ref' must be a boolean.")

        self.attr_name = 'id' if ref else 'json'

        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, self.type):
            raise self.make_error('type', type_name=self.type_name)

        entity = getattr(value, self.attr_name)
        if entity is None:
            raise self.make_error('attr', attr_name=self.attr_name)

        return entity


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
