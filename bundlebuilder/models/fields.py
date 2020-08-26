import datetime as dt

from marshmallow import fields

from .entity import (
    BaseEntity,
    PrimaryEntity,
    SecondaryEntity,
)


class EntityField(fields.Field):
    default_error_messages = {'invalid': 'Not a valid CTIM {type_name}.'}

    def __init__(self, **kwargs):
        self.type = kwargs.pop('type', None)
        if not (
            isinstance(self.type, type) and issubclass(self.type, BaseEntity)
        ):
            raise ValueError(f"'type' must be a subclass of {BaseEntity}.")

        self.type_name = (
            'Entity'  # abstract
            if self.type in (BaseEntity, PrimaryEntity, SecondaryEntity) else
            self.type.__name__  # concrete
        )

        ref = kwargs.pop('ref', False) and issubclass(self.type, PrimaryEntity)

        self.attr = 'id' if ref else 'json'

        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, self.type):
            return getattr(value, self.attr)

        raise self.make_error('invalid', type_name=self.type_name)


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
