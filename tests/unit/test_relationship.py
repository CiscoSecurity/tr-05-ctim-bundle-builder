from datetime import datetime

from marshmallow import ValidationError
from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    RELATIONSHIP_TYPE_CHOICES,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
)
from bundlebuilder.models import (
    Relationship,
    Judgement,
    Indicator,
)
from .utils import mock_id, mock_external_id


def test_relationship_validation_fails():
    data = {
        'greeting': '¡Hola!',
        'id': None,
        'relationship_type': 'loved-by',
        'target_ref': 3.141592653589793,
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_ids': ['foo', 'bar'],
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'language': 'Python',
        'revision': -273,
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'source': '',
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Relationship(**data)

    error = exc_info.value

    assert error.messages == {
        'greeting': ['Unknown field.'],
        'id': ['Field may not be null.'],
        'relationship_type': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, RELATIONSHIP_TYPE_CHOICES))
            )
        ],
        'source_ref': ['Missing data for required field.'],
        'target_ref': ['Not a valid string or a CTIM entity.'],
        'external_references': {
            0: {
                'source_name': ['Missing data for required field.'],
                'description': ['Field may not be blank.'],
                'external_id': ['Field may not be null.'],
            }
        },
        'revision': [
            'Must be greater than or equal to {}.'.format(
                REVISION_MIN_VALUE
            )
        ],
        'short_description': [
            'Must be at most {} characters long.'.format(
                SHORT_DESCRIPTION_LENGTH
            )
        ],
        'source': ['Field may not be blank.'],
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, TLP_CHOICES))
            )
        ],
    }

    assert error.valid_data == {
        'external_ids': ['foo', 'bar'],
        'external_references': [{
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'language': 'Python',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
    }


def test_relationship_validation_succeeds():
    judgement = Judgement()

    indicator = Indicator()

    # Python datetime objects don't have time zone info by default,
    # and without it, Python actually violates the ISO 8601 specification.
    timestamp = datetime.utcnow().isoformat() + 'Z'

    relationship = Relationship(
        relationship_type='based-on',
        source_ref=judgement,
        target_ref=indicator,
        revision=1,
        timestamp=timestamp,
        tlp='green',
    )

    assert relationship.json == {
        'type': 'relationship',
        'schema_version': SCHEMA_VERSION,
        'id': mock_id('relationship'),
        'relationship_type': 'based-on',
        'source_ref': judgement.id,
        'target_ref': indicator.id,
        'external_ids': [mock_external_id('relationship')],
        'revision': 1,
        'timestamp': timestamp,
        'tlp': 'green',
    }
