from functools import partial

from marshmallow import Schema, fields

from .validators import (
    validate_string,
    validate_datetime,
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
    start_time = fields.String(
        validate=validate_datetime,
        required=True,
    )
    end_time = fields.String(
        validate=validate_datetime,
    )


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
    start_time = fields.String(
        validate=validate_datetime,
    )
    end_time = fields.String(
        validate=validate_datetime,
    )
