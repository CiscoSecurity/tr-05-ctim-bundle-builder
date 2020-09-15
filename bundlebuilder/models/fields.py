import datetime as dt
import typing as t

from marshmallow import fields as f
from marshmallow.exceptions import ValidationError

from .entity import BaseEntity


# The default implementation of the `__repr__` method inherited from the
# `marshmallow.fields.Field` class is too verbose and ugly, so customize it
# for different subclasses to make them look like valid type annotations.


class RawField(f.Raw):

    def __repr__(self):
        return 'Any'


class BooleanField(f.Boolean):

    def __repr__(self):
        return 'bool'


class IntegerField(f.Integer):

    def __repr__(self):
        return 'int'


class StringField(f.String):

    def __repr__(self):
        return 'str'


class ListField(f.List):

    def __repr__(self):
        return f'List[{repr(self.inner)}]'


class MappingField(f.Mapping):

    def __repr__(self):
        return f'Dict[{repr(self.key_field)}, {repr(self.value_field)}]'


class EntityField(f.Field):
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
            raise ValueError("'ref' must be a boolean.")

        self.attr_name = 'id' if ref else 'json'

        super().__init__(**kwargs)

    def __repr__(self):
        return self.type_name

    def _deserialize(
        self,
        value: t.Any,
        attr: t.Optional[str],
        data: t.Optional[t.Mapping[str, t.Any]],
        **kwargs
    ):
        if not isinstance(value, self.type):
            raise self.make_error('type', type_name=self.type_name)

        entity = getattr(value, self.attr_name)
        if entity is None:
            raise self.make_error('attr', attr_name=self.attr_name)

        return entity


class DateTimeField(f.NaiveDateTime):
    """A UTC datetime string with the Z suffix."""

    def __init__(self, **kwargs):
        kwargs['format'] = 'iso8601'
        kwargs['timezone'] = dt.timezone.utc
        super().__init__(**kwargs)

    def __repr__(self):
        return 'str'

    def _deserialize(
        self,
        value: t.Any,
        attr: t.Optional[str],
        data: t.Optional[t.Mapping[str, t.Any]],
        **kwargs
    ):
        if isinstance(value, dt.datetime):
            value = value.isoformat()

        # Validate as a proper ISO-formatted string,
        # but don't convert to a DateTime object.
        datetime = super()._deserialize(value, attr, data, **kwargs)

        return datetime.isoformat(timespec='milliseconds') + 'Z'


class UnionField(f.Field):

    def __init__(self, candidates: t.List[f.Field], **kwargs):
        self.candidates = candidates
        super().__init__(**kwargs)

    def __repr__(self):
        return f'Union[{", ".join(map(repr, self.candidates))}]'

    def _deserialize(
        self,
        value: t.Any,
        attr: t.Optional[str],
        data: t.Optional[t.Mapping[str, t.Any]],
        **kwargs
    ):
        messages = []

        for candidate in self.candidates:
            try:
                return candidate.deserialize(value, attr, data, **kwargs)
            except ValidationError as error:
                messages.extend(error.messages)

        raise ValidationError(messages)
