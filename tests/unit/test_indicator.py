from pytest import raises as assert_raises

from bundlebuilder.constants import (
    BOOLEAN_OPERATOR_CHOICES,
    CONFIDENCE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    INDICATOR_TYPE_CHOICES,
    KILL_CHAIN_PHASE_NAME_CHOICES,
    LIKELY_IMPACT_MAX_LENGTH,
    TEST_MECHANISM_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Indicator
from .utils import (
    mock_id,
    mock_external_id,
    utc_now_iso,
)


def test_indicator_validation_fails():
    indicator_data = {
        'greeting': '¡Hola!',
        'id': None,
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
        'external_ids': ['foo', 'bar'],
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'indicator_type': ['Californication', 'Anonymization', 'Exfiltration'],
        'kill_chain_phases': [{'phase_name': 'divide-and-conquer'}],
        'language': 'Python',
        'likely_impact': '\U0001f4a9' * (LIKELY_IMPACT_MAX_LENGTH + 1),
        'negate': 69,
        'revision': -273,
        'severity': 'Insignificant',
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'source': '',
        'test_mechanisms': ['\U0001f4a9' * (TEST_MECHANISM_MAX_LENGTH + 1)],
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exception_info:
        Indicator(**indicator_data)

    error = exception_info.value

    assert error.data == {
        'greeting': ['Unknown field.'],
        'id': ['Field may not be null.'],
        'producer': ['Missing data for required field.'],
        'valid_time': {
            'middle_time': ['Unknown field.'],
        },
        'composite_indicator_expression': {
            'operator': [
                'Must be one of: {}.'.format(
                    ', '.join(map(repr, BOOLEAN_OPERATOR_CHOICES))
                )
            ],
        },
        'confidence': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, CONFIDENCE_CHOICES))
            )
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
                'Must be one of: {}.'.format(
                    ', '.join(map(repr, INDICATOR_TYPE_CHOICES))
                )
            ],
        },
        'kill_chain_phases': {
            0: {
                'kill_chain_name': ['Missing data for required field.'],
                'phase_name': [
                    'Must be one of: {}.'.format(
                        ', '.join(map(repr, KILL_CHAIN_PHASE_NAME_CHOICES))
                    )
                ],
            },
        },
        'likely_impact': [
            'Must be at most {} characters long.'.format(
                LIKELY_IMPACT_MAX_LENGTH
            )
        ],
        'negate': ['Not a valid boolean.'],
        'revision': [
            'Must be greater than or equal to {}.'.format(REVISION_MIN_VALUE)
        ],
        'severity': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, SEVERITY_CHOICES))
            )
        ],
        'short_description': [
            'Must be at most {} characters long.'.format(
                SHORT_DESCRIPTION_LENGTH
            )
        ],
        'source': ['Field may not be blank.'],
        'test_mechanisms': {
            0: [
                'Must be at most {} characters long.'.format(
                    TEST_MECHANISM_MAX_LENGTH
                )
            ],
        },
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, TLP_CHOICES))
            )
        ],
    }


def test_indicator_validation_succeeds():
    indicator_data = {
        'producer': 'SoftServe',
        'confidence': 'High',
        'valid_time': {'start_time': utc_now_iso()},
        'indicator_type': ['File Hash Watchlist'],
        'kill_chain_phases': [{
            'kill_chain_name': 'kill-chain-name',
            'phase_name': 'command-and-control',
        }],
        'negate': True,
        'revision': 0,
        'severity': 'High',
        'source': 'Python CTIM Bundle Builder : Indicator',
        'source_uri': (
            'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder'
        ),
        'tags': ['cisco', 'security', 'python', 'ctim', 'bundle', 'builder'],
        'timestamp': utc_now_iso(),
        'tlp': 'red',
    }

    indicator = Indicator(**indicator_data)

    assert indicator.json == {
        'type': 'indicator',
        'schema_version': SCHEMA_VERSION,
        'id': mock_id('indicator'),
        'external_ids': [mock_external_id('indicator')],
        **indicator_data
    }