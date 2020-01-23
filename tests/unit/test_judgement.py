from pytest import raises as assert_raises

from bundlebuilder.constants import (
    PRIORITY_MAX_VALUE,
    REASON_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    DISPOSITION_MAP,
    OBSERVABLE_TYPE_CHOICES,
    SEVERITY_CHOICES,
    REVISION_MIN_VALUE,
    TLP_CHOICES,
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Judgement
from .utils import (
    mock_id,
    mock_external_id,
    utc_now_iso,
)


def test_judgement_validation_fails():
    judgement_data = {
        'greeting': '¡Hola!',
        'confidence': 'Unbelievable',
        'disposition': 0,
        'disposition_name': 'Pristine',
        'observable': {
            'dangerous': False,
            'type': 'dummy',
        },
        'priority': PRIORITY_MAX_VALUE + 1,
        'severity': 'Insignificant',
        'valid_time': {
            'middle_time': 'This value will be ignored anyway, right?',
            'end_time': '1970-01-01T00:00:00Z',
        },
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'language': 'Python',
        'reason': '\U0001f4a9' * (REASON_MAX_LENGTH + 1),
        'revision': -273,
        'timestamp': '4:20',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Judgement(**judgement_data)

    error = exc_info.value

    assert error.data == {
        'greeting': ['Unknown field.'],
        'confidence': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, CONFIDENCE_CHOICES))
            )
        ],
        'disposition': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, DISPOSITION_MAP.keys()))
            )
        ],
        'disposition_name': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, DISPOSITION_MAP.values()))
            )
        ],
        'observable': {
            'dangerous': ['Unknown field.'],
            'type': [
                'Must be one of: {}.'.format(
                    ', '.join(map(repr, OBSERVABLE_TYPE_CHOICES))
                )
            ],
            'value': ['Missing data for required field.'],
        },
        'priority': [
            'Must be less than or equal to {}.'.format(PRIORITY_MAX_VALUE)
        ],
        'severity': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, SEVERITY_CHOICES))
            )
        ],
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'external_references': {
            0: {
                'source_name': ['Missing data for required field.'],
                'description': ['Field may not be blank.'],
                'external_id': ['Field may not be null.'],
            },
        },
        'reason': [
            'Must be at most {} characters long.'.format(
                REASON_MAX_LENGTH
            )
        ],
        'revision': [
            'Must be greater than or equal to {}.'.format(
                REVISION_MIN_VALUE
            )
        ],
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, TLP_CHOICES))
            )
        ],
    }


def test_judgement_validation_succeeds():
    judgment_data = {
        'confidence': 'Medium',
        'disposition': 3,
        'disposition_name': 'Suspicious',
        'observable': {'type': 'sha256', 'value': '01' * 32},
        'priority': 50,
        'severity': 'Medium',
        'valid_time': {'end_time': utc_now_iso()},
        'revision': 0,
        'timestamp': utc_now_iso(),
        'tlp': 'amber',
    }

    judgement = Judgement(**judgment_data)

    expected_type = 'judgement'

    assert judgement.json == {
        'type': expected_type,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, expected_type)
        ],
        **judgment_data
    }
