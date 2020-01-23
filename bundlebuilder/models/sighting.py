from functools import partial
from typing import List

from marshmallow import fields
from marshmallow.schema import Schema

from .entity import Entity
from .utils.fields import DateTimeField
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
    observed_time = fields.Nested(
        ObservedTimeSchema,
        required=True,
    )
    data = fields.Nested(SightingDataTableSchema)
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
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
    targets = fields.List(
        fields.Nested(IdentitySpecificationSchema)
    )
    timestamp = DateTimeField()
    title = fields.String(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = fields.String(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    external_id_extra_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Sighting(Entity):
    schema = SightingSchema

    @property
    def external_id_seed_values(self) -> List[str]:
        return [
            self.external_id_prefix,
            self.type,
        ]
