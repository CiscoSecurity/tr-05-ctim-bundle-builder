from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    COLUMN_TYPE_CHOICES,
    COUNT_MIN_VALUE,
    OBSERVABLE_TYPE_CHOICES,
    OBSERVABLE_RELATION_CHOICES,
    RESOLUTION_CHOICES,
    REVISION_MIN_VALUE,
    SENSOR_CHOICES,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import Sighting
from .utils import (
    mock_id,
    mock_external_id,
    utc_now_iso,
)


def test_sighting_validation_fails():
    sighting_data = {
        'greeting': '¡Hola!',
        'confidence': 'Unbelievable',
        'id': None,
        'observed_time': {
            'middle_time': 'This value will be ignored anyway, right?',
            'end_time': '1970-01-01T00:00:00Z',
        },
        'data': {
            'column_count': +1,
            'columns': [{'type': 'anything'}],
            'rows': [''],
            'row_count': -1,
        },
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_ids': ['foo', 'bar'],
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'internal': 69,
        'language': 'Python',
        'observables': [{
            'dangerous': False,
            'type': 'dummy',
        }],
        'relations': [{
            'score': 4.61,
            'related': {'type': 'device', 'value': 'iphone'},
            'relation': 'Is_Fond_Of',
            'source': {'type': 'user', 'value': 'admin'},
        }],
        'resolution': 'skipped',
        'revision': -273,
        'sensor': 'actuator',
        'sensor_coordinates':  [{
            'location': 'Europe',
            'observables': [{'type': 'ip', 'value': '127.0.0.1'}],
            'type': 'actuator',
        }],
        'severity': 'Insignificant',
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'source': '',
        'targets': [{
            'observed_time': {'start_time': '1970-01-01T00:00:00Z'},
            'type': 'actuator',
        }],
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exception_info:
        Sighting(**sighting_data)

    error = exception_info.value

    assert error.data == {
        'greeting': ['Unknown field.'],
        'confidence': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, CONFIDENCE_CHOICES))
            )
        ],
        'count': ['Missing data for required field.'],
        'id': ['Field may not be null.'],
        'observed_time': {
            'start_time': ['Missing data for required field.'],
            'middle_time': ['Unknown field.'],
        },
        'data': {
            'column_count': ['Unknown field.'],
            'columns': {
                0: {
                    'name': ['Missing data for required field.'],
                    'type': [
                        'Must be one of: {}.'.format(
                            ', '.join(map(repr, COLUMN_TYPE_CHOICES))
                        )
                    ],
                }
            },
            'rows': {
                0: ['Not a valid list.'],
            },
            'row_count': [
                'Must be greater than or equal to {}.'.format(COUNT_MIN_VALUE)
            ],
        },
        'external_references': {
            0: {
                'source_name': ['Missing data for required field.'],
                'description': ['Field may not be blank.'],
                'external_id': ['Field may not be null.'],
            },
        },
        'internal': ['Not a valid boolean.'],
        'observables': {
            0: {
                'dangerous': ['Unknown field.'],
                'type': [
                    'Must be one of: {}.'.format(
                        ', '.join(map(repr, OBSERVABLE_TYPE_CHOICES))
                    )
                ],
                'value': ['Missing data for required field.'],
            },
        },
        'relations': {
            0: {
                'score': ['Unknown field.'],
                'origin': ['Missing data for required field.'],
                'relation': [
                    'Must be one of: {}.'.format(
                        ', '.join(map(repr, OBSERVABLE_RELATION_CHOICES))
                    )
                ],
            }
        },
        'resolution': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, RESOLUTION_CHOICES))
            )
        ],
        'revision': [
            'Must be greater than or equal to {}.'.format(
                REVISION_MIN_VALUE
            )
        ],
        'sensor': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, SENSOR_CHOICES))
            )
        ],
        'sensor_coordinates': {
            0: {
                'location': ['Unknown field.'],
                'type': [
                    'Must be one of: {}.'.format(
                        ', '.join(map(repr, SENSOR_CHOICES))
                    )
                ],
            },
        },
        'severity':  [
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
        'targets': {
            0: {
                'observables': ['Missing data for required field.'],
                'type': [
                    'Must be one of: {}.'.format(
                        ', '.join(map(repr, SENSOR_CHOICES))
                    )
                ],
            },
        },
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            'Must be one of: {}.'.format(
                ', '.join(map(repr, TLP_CHOICES))
            )
        ],
    }


def test_sighting_validation_succeeds():
    sighting_data = {
        'confidence': 'Medium',
        'count': 2,
        'observed_time': {'start_time': utc_now_iso()},
        'data': {
            'columns': [
                {'name': 'full_name', 'type': 'string', 'required': True},
                {'name': 'country', 'type': 'string', 'required': False},
                {'name': 'year_of_birth', 'type': 'integer'},
            ],
            'rows': [
                ['Gevorg Davoian', 'Ukraine', 1993],
            ],
        },
        'internal': True,
        'observables': [{'type': 'domain', 'value': 'cisco.com'}],
        'relations': [{
            'origin': 'A bad URL redirecting to a good one.',
            'related': {'type': 'url', 'value': 'https://fake.org/good.html'},
            'relation': 'Redirects_To',
            'source': {'type': 'url', 'value': 'https://fake.org/bad.html'},
        }],
        'resolution': 'detected',
        'revision': 0,
        'sensor': 'network.firewall',
        'sensor_coordinates': [{
            'observables': [{'type': 'email', 'value': 'username@gmail.com'}],
            'type': 'endpoint.laptop',
            'os': 'Linux',
        }],
        'source': 'Python CTIM Bundle Builder : Sighting',
        'source_uri': (
            'https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder'
        ),
        'targets': [{
            'observables': [{'type': 'sha256', 'value': '01' * 32}],
            'observed_time': {'start_time': utc_now_iso()},
            'type': 'process.anti-virus-scanner',
            'os': 'Windows',
        }],
        'timestamp': utc_now_iso(),
        'tlp': 'amber',
    }

    sighting = Sighting(**sighting_data)

    assert sighting.json == {
        'type': 'sighting',
        'schema_version': SCHEMA_VERSION,
        'id': mock_id('sighting'),
        'external_ids': [mock_external_id('sighting')],
        **sighting_data
    }
