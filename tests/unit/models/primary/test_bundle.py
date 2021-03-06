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
    ObservedTime,
    Observable,
    Judgement,
    ValidTime,
    Indicator,
    Relationship,
    Verdict,
)
from bundlebuilder.session import Session
from tests.unit.utils import (
    mock_transient_id,
    mock_external_id,
)


def test_bundle_validation_fails():
    bundle_data = {
        'greeting': '¡Hola!',
        'valid_time': object(),
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [object()],
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
        'verdicts': [object()],
    }

    with assert_raises(ValidationError) as exc_info:
        Bundle(**bundle_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'valid_time': ['Not a valid CTIM ValidTime.'],
        'external_references': {
            0: ['Not a valid CTIM ExternalReference.'],
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
        'verdicts': {
            0: ['Not a valid CTIM Verdict.'],
        },
    },)


def test_bundle_validation_succeeds():
    # Make sure to keep README up-to-date.

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
            observed_time=ObservedTime(
                start_time='2019-03-01T22:26:29.229Z',
            ),
            observables=[
                Observable(
                    type='ip',
                    value='187.75.16.75',
                ),
            ],
            severity='High',
            timestamp='2019-03-01T22:26:29.229Z',
            tlp='green',
        )

        bundle.add_sighting(sighting)

        judgement = Judgement(
            confidence='High',
            disposition=2,
            disposition_name='Malicious',
            observable=Observable(
                type='ip',
                value='187.75.16.75',
            ),
            priority=95,
            severity='High',
            valid_time=ValidTime(
                start_time='2019-03-01T22:26:29.229Z',
                end_time='2019-03-31T22:26:29.229Z',
            ),
            timestamp='2019-03-01T22:26:29.229Z',
            tlp='green',
        )

        bundle.add_judgement(judgement)

        indicator = Indicator(
            producer='Cisco TALOS',
            valid_time=ValidTime(
                start_time='2019-03-01T22:26:29.229Z',
                end_time='2525-01-01T00:00:00.000Z',
            ),
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
            short_description=f'{judgement} is based-on {indicator}',
        )

        bundle.add_relationship(relationship_from_judgement_to_indicator)

        relationship_from_sighting_to_indicator = Relationship(
            relationship_type='sighting-of',
            source_ref=sighting,
            target_ref=indicator,
            short_description=f'{sighting} is sighting-of {indicator}',
        )

        bundle.add_relationship(relationship_from_sighting_to_indicator)

        verdict = Verdict.from_judgement(judgement)

        bundle.add_verdict(verdict)

        bundle_data = {
            'sightings': [sighting.json],
            'judgements': [judgement.json],
            'indicators': [indicator.json],
            'relationships': [
                relationship_from_judgement_to_indicator.json,
                relationship_from_sighting_to_indicator.json,
            ],
            'verdicts': [verdict.json],
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
