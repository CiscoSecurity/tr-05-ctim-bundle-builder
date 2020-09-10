from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    CONFIDENCE_CHOICES,
    COLUMN_TYPE_CHOICES,
    COUNT_MIN_VALUE,
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
from bundlebuilder.models import (
    Sighting,
    Observable,
    ObservedRelation,
)
from tests.unit.utils import (
    mock_transient_id,
    mock_external_id,
    utc_now_iso,
)


def test_sighting_validation_fails():
    sighting_data = {
        'greeting': '¡Hola!',
        'confidence': 'Unbelievable',
        'observed_time': {
            'middle_time': 'This value will be ignored anyway, right?',
            'end_time': '1970-01-01T00:00:00Z',
        },
        'data': {
            'column_count': +1,
            'columns': [{'type': 'anything'}],
            'rows': [object()],
            'row_count': -1,
        },
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [object()],
        'internal': 69,
        'language': 'Python',
        'observables': [object()],
        'relations': [object()],
        'resolution': 'skipped',
        'revision': -273,
        'sensor': 'actuator',
        'sensor_coordinates':  [{
            'location': 'Europe',
            'observables': [{'type': 'ip', 'value': '127.0.0.1'}],
        }],
        'severity': 'Insignificant',
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'targets': [{
            'local': True,
            'observed_time': {'start_time': '1970-01-01T00:00:00Z'},
            'type': 'thread.daemon',
        }],
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Sighting(**sighting_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'confidence': [
            f'Must be one of: {", ".join(map(repr, CONFIDENCE_CHOICES))}.'
        ],
        'count': ['Missing data for required field.'],
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
                        'Must be one of: '
                        f'{", ".join(map(repr, COLUMN_TYPE_CHOICES))}.'
                    ],
                }
            },
            'rows': {
                0: ['Not a valid list.'],
            },
            'row_count': [
                f'Must be greater than or equal to {COUNT_MIN_VALUE}.'
            ],
        },
        'external_references': {
            0: ['Not a valid CTIM ExternalReference.'],
        },
        'internal': ['Not a valid boolean.'],
        'observables': {
            0: ['Not a valid CTIM Observable.'],
        },
        'relations': {
            0: ['Not a valid CTIM ObservedRelation.'],
        },
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'sensor_coordinates': {
            0: {
                'location': ['Unknown field.'],
                'type': ['Missing data for required field.'],
            },
        },
        'severity':  [
            f'Must be one of: {", ".join(map(repr, SEVERITY_CHOICES))}.'
        ],
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
        'targets': {
            0: {
                'local': ['Unknown field.'],
                'observables': ['Missing data for required field.'],
            },
        },
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_sighting_validation_succeeds():
    observable = Observable(
        type='domain',
        value='cisco.com',
    )

    relation = ObservedRelation(
        origin='A bad URL redirecting to a good one.',
        related=Observable(
            type='url',
            value='https://fake.org/good.html',
        ),
        relation='Redirects_To',
        source=Observable(
            type='url',
            value='https://fake.org/bad.html',
        ),
    )

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
        'observables': [observable],
        'relations': [relation],
        'resolution': 'detected',
        'revision': 0,
        'sensor': 'network.firewall',
        'sensor_coordinates': [{
            'observables': [{'type': 'email', 'value': 'username@gmail.com'}],
            'type': 'endpoint.laptop',
            'os': 'Linux',
        }],
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

    sighting_data['observables'] = [observable.json]
    sighting_data['relations'] = [relation.json]

    type_ = 'sighting'

    assert sighting.json == {
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': DEFAULT_SESSION_SOURCE,
        'source_uri': DEFAULT_SESSION_SOURCE_URI,
        'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
        'external_ids': [
            mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
        ],
        **sighting_data
    }
