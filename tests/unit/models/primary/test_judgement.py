from pytest import raises as assert_raises

from bundlebuilder.constants import (
    PRIORITY_MAX_VALUE,
    REASON_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    DISPOSITION_MAP,
    SEVERITY_CHOICES,
    REVISION_MIN_VALUE,
    TLP_CHOICES,
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Judgement,
    Observable,
)
from tests.unit.utils import (
    mock_transient_id,
    mock_external_id,
    utc_now_iso,
)


def test_judgement_validation_fails():
    judgement_data = {
        'greeting': '¡Hola!',
        'confidence': 'Unbelievable',
        'disposition': 0,
        'disposition_name': 'Pristine',
        'observable': object(),
        'priority': PRIORITY_MAX_VALUE + 1,
        'severity': 'Insignificant',
        'valid_time': {
            'start_time': '1970-01-01T00:00:00Z',
            'middle_time': 'This value will be ignored anyway, right?',
        },
        'external_references': [object()],
        'language': 'Python',
        'reason': '\U0001f4a9' * (REASON_MAX_LENGTH + 1),
        'revision': -273,
        'timestamp': '4:20',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Judgement(**judgement_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'confidence': [
            f'Must be one of: {", ".join(map(repr, CONFIDENCE_CHOICES))}.'
        ],
        'disposition': [
            f'Must be one of: { ", ".join(map(repr, DISPOSITION_MAP.keys()))}.'
        ],
        'disposition_name': [
            'Must be one of: '
            f'{", ".join(map(repr, DISPOSITION_MAP.values()))}.'
        ],
        'observable': ['Not a valid CTIM Observable.'],
        'priority': [
            f'Must be less than or equal to {PRIORITY_MAX_VALUE}.'
        ],
        'severity': [
            f'Must be one of: {", ".join(map(repr, SEVERITY_CHOICES))}.'
        ],
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'external_references': {
            0: ['Not a valid CTIM ExternalReference.'],
        },
        'reason': [
            f'Must be at most {REASON_MAX_LENGTH} characters long.'
        ],
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_judgement_validation_succeeds():
    observable = Observable(
        type='domain',
        value='cisco.com',
    )

    judgement_data = {
        'confidence': 'Medium',
        'disposition': 3,
        'disposition_name': 'Suspicious',
        'observable': observable,
        'priority': 50,
        'severity': 'Medium',
        'valid_time': {'end_time': utc_now_iso()},
        'revision': 0,
        'timestamp': utc_now_iso(),
        'tlp': 'amber',
    }

    judgement = Judgement(**judgement_data)

    judgement_data['observable'] = observable.json

    type_ = 'judgement'

    assert judgement.json == {
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
        ],
        **judgement_data
    }
