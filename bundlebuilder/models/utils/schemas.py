from functools import partial

from marshmallow import fields
from marshmallow.decorators import (
    validates_schema,
    post_load,
)
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema

from .fields import DateTimeField
from .validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    SOURCE_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    COLUMN_TYPE_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    COUNT_MIN_VALUE,
    OBSERVABLE_TYPE_CHOICES,
    OBSERVABLE_RELATION_CHOICES,
    SENSOR_CHOICES,
    BOOLEAN_OPERATOR_CHOICES,
    KILL_CHAIN_PHASE_NAME_CHOICES,
)


class ExternalReferenceSchema(Schema):
    source_name = fields.String(
        validate=partial(validate_string, max_length=SOURCE_NAME_MAX_LENGTH),
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_id = fields.String(
        validate=validate_string,
    )
    hashes = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    url = fields.String(
        validate=validate_string,
    )


class ObservedTimeSchema(Schema):
    start_time = DateTimeField(required=True)
    end_time = DateTimeField()

    @validates_schema
    def validate_time_period(self, data, **kwargs):
        if not ('start_time' in data and 'end_time' in data):
            return

        if data['start_time'] > data['end_time']:
            message = 'Not a valid period of time: start must be before end.'
            raise ValidationError(message)


class ColumnDefinitionSchema(Schema):
    name = fields.String(
        validate=validate_string,
        required=True,
    )
    type = fields.String(
        validate=partial(validate_string, choices=COLUMN_TYPE_CHOICES),
        required=True,
    )
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH)
    )
    required = fields.Boolean()
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )


class SightingDataTableSchema(Schema):
    columns = fields.List(
        fields.Nested(ColumnDefinitionSchema),
        required=True,
    )
    rows = fields.List(
        fields.List(fields.Raw),
        required=True,
    )
    row_count = fields.Integer(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE)
    )


class ObservableSchema(Schema):
    type = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_TYPE_CHOICES),
        required=True,
    )
    value = fields.String(
        validate=validate_string,
        required=True,
    )


class ObservedRelationSchema(Schema):
    origin = fields.String(
        validate=validate_string,
        required=True,
    )
    related = fields.Nested(
        ObservableSchema,
        required=True,
    )
    relation = fields.String(
        validate=partial(validate_string, choices=OBSERVABLE_RELATION_CHOICES),
        required=True,
    )
    source = fields.Nested(
        ObservableSchema,
        required=True,
    )
    origin_uri = fields.String(
        validate=validate_string,
    )
    relation_info = fields.Mapping(
        keys=fields.String,
        values=fields.Raw,
    )


class SensorCoordinatesSchema(Schema):
    observables = fields.List(
        fields.Nested(ObservableSchema),
        required=True,
    )
    type = fields.String(
        validate=partial(validate_string, choices=SENSOR_CHOICES),
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class IdentitySpecificationSchema(Schema):
    observables = fields.List(
        fields.Nested(ObservableSchema),
        required=True,
    )
    observed_time = fields.Nested(
        ObservedTimeSchema,
        required=True,
    )
    type = fields.String(
        validate=partial(validate_string, choices=SENSOR_CHOICES),
        required=True,
    )
    os = fields.String(
        validate=validate_string,
    )


class ValidTimeSchema(Schema):
    start_time = DateTimeField()
    end_time = DateTimeField()

    @validates_schema
    def validate_time_period(self, data, **kwargs):
        if not ('start_time' in data and 'end_time' in data):
            return

        if data['start_time'] > data['end_time']:
            message = 'Not a valid period of time: start must be before end.'
            raise ValidationError(message)


class CompositeIndicatorExpressionSchema(Schema):
    indicator_ids = fields.List(
        fields.String(
            validate=validate_string,
        ),
        required=True,
    )
    operator = fields.String(
        validate=partial(validate_string, choices=BOOLEAN_OPERATOR_CHOICES),
        required=True,
    )


class KillChainPhaseSchema(Schema):
    kill_chain_name = fields.String(
        validate=validate_string,
        required=True,
    )
    phase_name = fields.String(
        validate=partial(
            validate_string,
            choices=KILL_CHAIN_PHASE_NAME_CHOICES,
        ),
        required=True,
    )

    @post_load
    def normalize_kill_chain_name(self, data, **kwargs):
        if 'kill_chain_name' in data:
            value = data['kill_chain_name']
            value = value.lower().strip().split()
            value = ' '.join(value)
            value = value.replace(' ', '_').replace('_', '-')
            data['kill_chain_name'] = value
        return data
