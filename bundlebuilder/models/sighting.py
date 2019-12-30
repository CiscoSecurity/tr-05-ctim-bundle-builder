from functools import partial

from marshmallow import Schema, fields

from .entity import Entity
from .utils.schemas import (
    ObservedTimeSchema,
    SightingDataTableSchema,
    ExternalReferenceSchema,
    ObservableSchema,
    ObservedRelationSchema,
    SensorCoordinatesSchema,
    IdentitySpecificationSchema,
)
from .utils.validators import (
    validate_string,
    validate_integer,
    validate_datetime,
)
from ..constants import (
    CONFIDENCE_CHOICES,
    COUNT_MIN_VALUE,
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    RESOLUTION_CHOICES,
    REVISION_MIN_VALUE,
    SENSOR_CHOICES,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class SightingSchema(Schema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/sighting.md
    """
    confidence = fields.String(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
        required=True,
    )
    count = fields.Integer(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE),
        required=True,
    )
    id = fields.String(
        validate=validate_string,
    )
    observed_time = fields.Nested(
        ObservedTimeSchema,
        required=True,
    )
    data = fields.Nested(SightingDataTableSchema)
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_ids = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    external_references = fields.List(
        fields.Nested(ExternalReferenceSchema)
    )
    internal = fields.Boolean()
    language = fields.String(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    observables = fields.List(
        fields.Nested(ObservableSchema)
    )
    relations = fields.List(
        fields.Nested(ObservedRelationSchema)
    )
    resolution = fields.String(
        validate=partial(validate_string, choices=RESOLUTION_CHOICES),
    )
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    sensor = fields.String(
        validate=partial(validate_string, choices=SENSOR_CHOICES),
    )
    sensor_coordinates = fields.List(
        fields.Nested(SensorCoordinatesSchema)
    )
    severity = fields.String(
        validate=partial(validate_string, choices=SEVERITY_CHOICES),
    )
    short_description = fields.String(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = fields.String(
        validate=validate_string,
    )
    targets = fields.List(
        fields.Nested(IdentitySpecificationSchema)
    )
    timestamp = fields.String(
        validate=validate_datetime,
    )
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )


class Sighting(Entity):
    schema = SightingSchema

    def generate_external_id_seed(self):
        # TODO: replace with real implementation
        return ''
