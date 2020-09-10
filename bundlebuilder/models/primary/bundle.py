from functools import partial
from typing import (
    Iterator,
    Tuple,
)

from marshmallow.exceptions import (
    ValidationError as MarshmallowValidationError
)

from ..entity import (
    EntitySchema,
    PrimaryEntity,
)
from ..fields import (
    EntityField,
    StringField,
    ListField,
    IntegerField,
    DateTimeField,
)
from ..primary.indicator import Indicator
from ..primary.judgement import Judgement
from ..primary.relationship import Relationship
from ..primary.sighting import Sighting
from ..primary.verdict import Verdict
from ..secondary.external_reference import ExternalReference
from ..secondary.valid_time import ValidTime
from ..validators import (
    validate_string,
    validate_integer,
)
from ...constants import (
    SOURCE_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    LANGUAGE_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TITLE_MAX_LENGTH,
    TLP_CHOICES,
)
from ...exceptions import (
    ValidationError as BundleBuilderValidationError
)


class BundleSchema(EntitySchema):
    """
    https://github.com/threatgrid/ctim/blob/master/doc/structures/bundle.md
    """

    valid_time = EntityField(type=ValidTime)
    description = StringField(
        validate=partial(validate_string, max_length=DESCRIPTION_MAX_LENGTH),
    )
    external_references = ListField(
        EntityField(type=ExternalReference)
    )
    indicator_refs = ListField(
        EntityField(type=Indicator, ref=True)
    )
    indicators = ListField(
        EntityField(type=Indicator)
    )
    judgement_refs = ListField(
        EntityField(type=Judgement, ref=True)
    )
    judgements = ListField(
        EntityField(type=Judgement)
    )
    language = StringField(
        validate=partial(validate_string, max_length=LANGUAGE_MAX_LENGTH),
    )
    relationship_refs = ListField(
        EntityField(type=Relationship, ref=True)
    )
    relationships = ListField(
        EntityField(type=Relationship)
    )
    revision = IntegerField(
        validate=partial(validate_integer, min_value=REVISION_MIN_VALUE),
    )
    short_description = StringField(
        validate=partial(validate_string, max_length=SHORT_DESCRIPTION_LENGTH),
    )
    sighting_refs = ListField(
        EntityField(type=Sighting, ref=True)
    )
    sightings = ListField(
        EntityField(type=Sighting)
    )
    timestamp = DateTimeField()
    title = StringField(
        validate=partial(validate_string, max_length=TITLE_MAX_LENGTH),
    )
    tlp = StringField(
        validate=partial(validate_string, choices=TLP_CHOICES),
    )
    verdict_refs = ListField(
        EntityField(type=Verdict, ref=True)
    )
    verdicts = ListField(
        EntityField(type=Verdict)
    )

    source = StringField(
        validate=partial(validate_string, max_length=SOURCE_MAX_LENGTH),
    )
    source_uri = StringField(
        validate=validate_string,
    )

    external_id_salt_values = ListField(
        StringField(
            validate=validate_string,
        )
    )
    external_ids = ListField(
        StringField(
            validate=validate_string,
        )
    )


class Bundle(PrimaryEntity):
    schema = BundleSchema

    def add_indicator(self, indicator: Indicator, ref: bool = False) -> None:
        self._add(indicator, Indicator, ref)

    def add_judgement(self, judgement: Judgement, ref: bool = False) -> None:
        self._add(judgement, Judgement, ref)

    def add_relationship(self, relationship: Relationship, ref: bool = False) -> None:  # noqa: E501
        self._add(relationship, Relationship, ref)

    def add_sighting(self, sighting: Sighting, ref: bool = False) -> None:
        self._add(sighting, Sighting, ref)

    def add_verdict(self, verdict: Verdict, ref: bool = False) -> None:
        self._add(verdict, Verdict, ref)

    def _add(self, entity, type_, ref):
        try:
            field = EntityField(type=type_, ref=ref)
            data = field.deserialize(entity)
        except MarshmallowValidationError as error:
            raise BundleBuilderValidationError(*error.args) from error
        else:
            key = type_.type + ('_refs' if ref else 's')
            self.json.setdefault(key, []).append(data)

    def _generate_external_id_seed_values(self) -> Iterator[Tuple[str]]:
        yield (
            self.type,
        )
