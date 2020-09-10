from marshmallow.decorators import validates_schema
from marshmallow.exceptions import ValidationError

from ..entity import (
    EntitySchema,
    SecondaryEntity,
)
from ..fields import DateTimeField


class ValidTimeSchema(EntitySchema):
    start_time = DateTimeField()
    end_time = DateTimeField()

    @validates_schema
    def validate_time_period(self, data, **kwargs):
        if not ('start_time' in data and 'end_time' in data):
            return

        if data['start_time'] > data['end_time']:
            message = 'Not a valid period of time: start must come before end.'
            raise ValidationError(message)


class ValidTime(SecondaryEntity):
    schema = ValidTimeSchema
