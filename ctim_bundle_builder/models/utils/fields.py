from marshmallow import fields

from ..entity import Entity


class EntityRefField(fields.String):
    default_error_messages = {
        'invalid': 'Not a valid string or a CTIM entity.',
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, Entity):
            value = value.json['id']
        return super()._deserialize(value, attr, data, **kwargs)
