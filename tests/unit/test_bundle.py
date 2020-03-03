from pytest import raises as assert_raises

from bundlebuilder.constants import (
    DESCRIPTION_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Bundle,
    Sighting,
    Judgement,
    Indicator,
    Relationship,
)
from bundlebuilder.session import Session
from .utils import (
    mock_transient_id,
    mock_external_id,
)


def test_bundle_validation_fails():
    bundle_data = {
        'greeting': '¡Hola!',
        'valid_time': {
            'middle_time': 'This value will be ignored anyway, right?',
            'end_time': '1970-01-01T00:00:00Z',
        },
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [{
            'description': '',
            'external_id': None,
            'hashes': ['alpha', 'beta', 'gamma'],
        }],
        'indicators': [object()],
        'judgements': [object()],
        'language': 'Python',
        'relationships': [object()],
        'revision': -273,
        'sightings': [object()],
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Bundle(**bundle_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
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
        'indicators': {
            0: ['Not a valid CTIM Indicator.'],
        },
        'judgements': {
            0: ['Not a valid CTIM Judgement.'],
        },
        'relationships': {
            0: ['Not a valid CTIM Relationship.'],
        },
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'sightings': {
            0: ['Not a valid CTIM Sighting.'],
        },
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_bundle_validation_succeeds():
    # https://github.com/threatgrid/ctim/blob/master/doc/tutorials/modeling-threat-intel-ctim.md#173-example-bundle

    session = Session(
        external_id_prefix='ctim-tutorial',
        source='Modeling Threat Intelligence in CTIM Tutorial',
        source_uri=(
            'https://github.com/threatgrid/ctim/blob/master/'
            'doc/tutorials/modeling-threat-intel-ctim.md'
        ),
    )

    with session.set():
        bundle = Bundle()

        sighting = Sighting(
            confidence='High',
            count=1,
            observed_time={'start_time': '2019-03-01T22:26:29.229Z'},
            observables=[{'type': 'ip', 'value': '187.75.16.75'}],
            severity='High',
            timestamp='2019-03-01T22:26:29.229Z',
            tlp='green',
        )

        bundle.add_sighting(sighting)

        judgement = Judgement(
            confidence='High',
            disposition=2,
            disposition_name='Malicious',
            observable={'type': 'ip', 'value': '187.75.16.75'},
            priority=95,
            severity='High',
            valid_time={
                'start_time': '2019-03-01T22:26:29.229Z',
                'end_time': '2019-03-31T22:26:29.229Z',
            },
            timestamp='2019-03-01T22:26:29.229Z',
            tlp='green',
        )

        bundle.add_judgement(judgement)

        indicator = Indicator(
            producer='Cisco TALOS',
            valid_time={
                'start_time': '2019-03-01T22:26:29.229Z',
                'end_time': '2525-01-01T00:00:00.000Z',
            },
            description=(
                'The IP Blacklist is automatically updated every 15 minutes '
                'and contains a list of known malicious network threats that '
                'are flagged on all Cisco Security Products. This list is '
                'estimated to be 1% of the total Talos IP Reputation System.'
            ),
            short_description=(
                'The TALOS IP Blacklist lists all known malicious IPs in the '
                'TALOS IP Reputation System.'
            ),
            title='TALOS IP Blacklist Feed',
            tlp='green',
        )

        bundle.add_indicator(indicator)

        relationship_from_judgement_to_indicator = Relationship(
            relationship_type='based-on',
            source_ref=judgement,
            target_ref=indicator,
            short_description=(
                f'judgement {judgement} is based-on indicator {indicator}'
            ),
        )

        bundle.add_relationship(relationship_from_judgement_to_indicator)

        relationship_from_sighting_to_indicator = Relationship(
            relationship_type='sighting-of',
            source_ref=sighting,
            target_ref=indicator,
            short_description=(
                f'sighting {sighting} is sighting-of indicator {indicator}'
            ),
        )

        bundle.add_relationship(relationship_from_sighting_to_indicator)

        bundle_data = {
            'sightings': [sighting.json],
            'judgements': [judgement.json],
            'indicators': [indicator.json],
            'relationships': [
                relationship_from_judgement_to_indicator.json,
                relationship_from_sighting_to_indicator.json,
            ],
        }

    type_ = 'bundle'

    assert bundle.json == {
        'type': type_,
        'schema_version': SCHEMA_VERSION,
        'source': session.source,
        'source_uri': session.source_uri,
        'id': mock_transient_id(session.external_id_prefix, type_),
        'external_ids': [mock_external_id(session.external_id_prefix, type_)],
        **bundle_data
    }
