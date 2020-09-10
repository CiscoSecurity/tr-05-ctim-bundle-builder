from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Relationship,
    Observable,
    Judgement,
    Indicator,
)
from tests.unit.utils import (
    mock_transient_id,
    mock_external_id,
    utc_now_iso,
)


def test_relationship_validation_fails():
    relationship_data = {
        'greeting': '¡Hola!',
        'relationship_type': 'loved-by',
        'target_ref': 3.141592653589793,
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [object()],
        'language': 'Python',
        'revision': -273,
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Relationship(**relationship_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'source_ref': ['Missing data for required field.'],
        'target_ref': ['Not a valid CTIM Entity.'],
        'external_references': {
            0: ['Not a valid CTIM ExternalReference.'],
        },
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_relationship_validation_succeeds():
    observable = Observable(
        type='domain',
        value='cisco.com',
    )

    judgement = Judgement(
        confidence='Low',
        disposition=4,
        disposition_name='Common',
        observable=observable,
        priority=25,
        severity='Low',
        valid_time={
            'start_time': utc_now_iso(),
            'end_time': utc_now_iso(),
        },
        revision=1,
        timestamp=utc_now_iso(),
        tlp='white',
    )

    indicator = Indicator(
        producer='SoftServe',
        valid_time={
            'start_time': utc_now_iso(),
            'end_time': utc_now_iso(),
        },
        revision=2,
        timestamp=utc_now_iso(),
        tlp='green',
    )

    relationship_data = {
        'relationship_type': 'based-on',
        'source_ref': judgement,
        'target_ref': indicator,
        'revision': 3,
        'timestamp': utc_now_iso(),
        'tlp': 'amber',
    }

    relationship = Relationship(**relationship_data)

    relationship_data.update({
        'source_ref': judgement.id,
        'target_ref': indicator.id,
    })

    type_ = 'relationship'

    assert relationship.json == {
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
        ],
        **relationship_data
    }
