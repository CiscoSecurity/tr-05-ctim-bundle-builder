from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    RELATIONSHIP_TYPE_CHOICES,
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
    Judgement,
    Indicator,
)
from .utils import (
    mock_id,
    mock_external_id,
    utc_now_iso,
)


def test_relationship_validation_fails():
    relationship_data = {
        'greeting': '¡Hola!',
        'relationship_type': 'loved-by',
        'target_ref': 3.141592653589793,
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
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

    assert error.data == {
        'greeting': ['Unknown field.'],
        'relationship_type': [
            'Must be one of: '
            f'{", ".join(map(repr, RELATIONSHIP_TYPE_CHOICES))}.'
        ],
        'source_ref': ['Missing data for required field.'],
        'target_ref': ['Not a valid string or a CTIM entity.'],
        'external_references': {
            0: {
                'source_name': ['Missing data for required field.'],
                'description': ['Field may not be blank.'],
                'external_id': ['Field may not be null.'],
            },
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
    }


def test_relationship_validation_succeeds():
    judgement = Judgement(
        confidence='Low',
        disposition=4,
        disposition_name='Common',
        observable={'type': 'domain', 'value': 'cisco.com'},
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

    expected_type = 'relationship'

    assert relationship.json == {
        'type': expected_type,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type)
        ],
        **relationship_data
    }
