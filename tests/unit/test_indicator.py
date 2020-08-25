from pytest import raises as assert_raises

from bundlebuilder.constants import (
    BOOLEAN_OPERATOR_CHOICES,
    CONFIDENCE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    INDICATOR_TYPE_CHOICES,
    LIKELY_IMPACT_MAX_LENGTH,
    TEST_MECHANISM_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Indicator
from .utils import (
    mock_transient_id,
    mock_external_id,
    utc_now_iso,
)


def test_indicator_validation_fails():
    indicator_data = {
        'greeting': '¡Hola!',
        'valid_time': {
            'start_time': '1970-01-01T00:00:00Z',
            'middle_time': 'This value will be ignored anyway, right?',
        },
        'composite_indicator_expression': {
            'indicator_ids': ['x', 'y', 'z'],
            'operator': 'xor',
        },
        'confidence': 'Unbelievable',
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'indicator_type': ['Californication', 'Anonymization', 'Exfiltration'],
        'kill_chain_phases': [{'algorithm_name': 'divide-and-conquer'}],
        'language': 'Python',
        'likely_impact': '\U0001f4a9' * (LIKELY_IMPACT_MAX_LENGTH + 1),
        'negate': 69,
        'revision': -273,
        'severity': 'Insignificant',
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'specification': {'type': 'ThreatBrain'},
        'test_mechanisms': ['\U0001f4a9' * (TEST_MECHANISM_MAX_LENGTH + 1)],
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Indicator(**indicator_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'producer': ['Missing data for required field.'],
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'composite_indicator_expression': {
            'operator': [
                'Must be one of: '
                f'{", ".join(map(repr, BOOLEAN_OPERATOR_CHOICES))}.'
            ],
        },
        'confidence': [
            f'Must be one of: {", ".join(map(repr, CONFIDENCE_CHOICES))}.'
        ],
        'external_references': {
            0: {
                'source_name': ['Missing data for required field.'],
                'description': ['Field may not be blank.'],
                'external_id': ['Field may not be null.'],
            },
        },
        'indicator_type': {
            0: [
                'Must be one of: '
                f'{", ".join(map(repr, INDICATOR_TYPE_CHOICES))}.'
            ],
        },
        'kill_chain_phases': {
            0: {
                'algorithm_name': ['Unknown field.'],
                'kill_chain_name': ['Missing data for required field.'],
                'phase_name': ['Missing data for required field.'],
            },
        },
        'likely_impact': [
            f'Must be at most {LIKELY_IMPACT_MAX_LENGTH} characters long.'
        ],
        'negate': ['Not a valid boolean.'],
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'severity': [
            f'Must be one of: {", ".join(map(repr, SEVERITY_CHOICES))}.'
        ],
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
        'specification': {
            'variables': ['Missing data for required field.'],
        },
        'test_mechanisms': {
            0: [
                f'Must be at most {TEST_MECHANISM_MAX_LENGTH} characters long.'
            ],
        },
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_indicator_validation_succeeds():
    judgement_id = 'transient:prefix-judgement-sha256'
    judgement_uri = (
        f'https://private.intel.amp.cisco.com/ctia/judgement/{judgement_id}'
    )

    indicator_data = {
        'producer': 'SoftServe',
        'confidence': 'High',
        'valid_time': {'start_time': utc_now_iso()},
        'indicator_type': ['File Hash Watchlist'],
        'kill_chain_phases': [{
            'kill_chain_name': 'Kill_Chain_Name',
            'phase_name': 'Phase Name',
        }],
        'negate': True,
        'revision': 0,
        'severity': 'High',
        'specification': {
            'type': 'Judgement',
            'judgements': [judgement_uri],
            'required_judgements': [{'judgement_id': judgement_id}],
        },
        'tags': ['cisco', 'security', 'python', 'ctim', 'bundle', 'builder'],
        'timestamp': utc_now_iso(),
        'tlp': 'red',
    }

    indicator = Indicator(**indicator_data)

    indicator_data['kill_chain_phases'][0].update({
        'kill_chain_name': 'kill-chain-name',
        'phase_name': 'phase-name',
    })

    type_ = 'indicator'

    assert indicator.json == {
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
        ],
        **indicator_data
    }
