from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..fields import (
    StringField,
    IntegerField,
    EntityField,
    ListField,
    BooleanField,
    DateTimeField,
)
from ..secondary.external_reference import ExternalReference
from ..secondary.identity_specification import IdentitySpecification
from ..secondary.observable import Observable
from ..secondary.observed_relation import ObservedRelation
from ..secondary.observed_time import ObservedTime
from ..secondary.sensor_coordinates import SensorCoordinates
from ..secondary.sighting_data_table import SightingDataTable
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

    confidence = StringField(
        validate=partial(validate_string, choices=CONFIDENCE_CHOICES),
        required=True,
    )
    count = IntegerField(
        validate=partial(validate_integer, min_value=COUNT_MIN_VALUE),
        required=True,
    )
    observed_time = EntityField(
        type=ObservedTime,
        required=True,
    )
    data = EntityField(
        type=SightingDataTable,
    )
    description = StringField(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = ListField(
        EntityField(type=ExternalReference)
    )
    internal = BooleanField()
    language = StringField(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    observables = ListField(
        EntityField(type=Observable)
    )
    relations = ListField(
        EntityField(type=ObservedRelation)
    )
    resolution = StringField(
        validate=validate_string,
    )
    revision = IntegerField(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    sensor = StringField(
        validate=validate_string,
    )
    sensor_coordinates = ListField(
        EntityField(type=SensorCoordinates)
    )
    severity = StringField(
        validate=partial(validate_string, choices=SEVERITY_CHOICES),
    )
    short_description = StringField(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    targets = ListField(
        EntityField(type=IdentitySpecification)
    )
    timestamp = DateTimeField()
    title = StringField(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = StringField(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )

    source = StringField(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = StringField(
        validate=validate_string,
    )

    external_id_salt_values = ListField(
        StringField(validate=validate_string)
    )
    external_ids = ListField(
        StringField(validate=validate_string)
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
