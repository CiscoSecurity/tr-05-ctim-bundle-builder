from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow import fields

from ..fields import (
    EntityField,
    DateTimeField,
)
from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..secondary.external_reference import ExternalReference
from ..secondary.observable import Observable
from ..secondary.observed_relation import ObservedRelation
from ..secondary.observed_time import ObservedTime
from ..secondary.sighting_data_table import SightingDataTable
from ..schemas import (
    SensorCoordinatesSchema,
    IdentitySpecificationSchema,
)
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    CONFIDENCE_CHOICES,
    COUNT_MIN_VALUE,
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    SOURCE_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)


class SightingSchema(EntitySchema):
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
    observed_time = EntityField(
        type=ObservedTime,
        required=True,
    )
    data = EntityField(type=SightingDataTable)
    description = fields.String(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = fields.List(
        EntityField(type=ExternalReference)
    )
    internal = fields.Boolean()
    language = fields.String(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    observables = fields.List(
        EntityField(type=Observable)
    )
    relations = fields.List(
        EntityField(type=ObservedRelation)
    )
    resolution = fields.String(
        validate=validate_string,
    )
    revision = fields.Integer(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    sensor = fields.String(
        validate=validate_string,
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

    source = fields.String(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = fields.String(
        validate=validate_string,
    )

    external_id_salt_values = fields.List(
        fields.String(
            validate=validate_string,
        )
    )
    external_ids = fields.List(
        fields.String(
            validate=validate_string,
        )
    )


class Sighting(PrimaryEntity):
    schema = SightingSchema

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        observables = self.observables or []

        if observables:
            for observable in observables:
                yield (
                    self.type,
                    self.title or '',
                    (self.timestamp or '').split('T', 1)[0],
                    observable['value'],
                )

        else:
            yield (
                self.type,
                self.title or '',
                (self.timestamp or '').split('T', 1)[0],
            )
