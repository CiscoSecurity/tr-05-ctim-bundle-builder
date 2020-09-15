[![Gitter Chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Threat-Response "Gitter Chat")
[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-ctim-bundle-builder.svg?branch=develop)](https://travis-ci.com/CiscoSecurity/tr-05-ctim-bundle-builder)
[![PyPi Version](https://img.shields.io/pypi/v/bundlebuilder.svg)](https://pypi.python.org/pypi/bundlebuilder)
[![Python Versions](https://img.shields.io/pypi/pyversions/bundlebuilder.svg)](https://pypi.python.org/pypi/bundlebuilder)

# Threat Response CTIM Bundle Builder

Python library for building CTIM entities, relationships between them, and
finally packaging everything up into so-called bundles.

Features (more details later):
- Support for sessions per each particular use of the tool.
- Validation of fields for CTIM entities according to the
[latest schemas](https://github.com/threatgrid/ctim/tree/master/doc/structures).
- Generation of transient IDs and external IDs (XIDs) according to the
[best practices](https://github.com/threatgrid/ctim/blob/master/doc/tutorials/modeling-threat-intel-ctim.md#1113-best-practices-for-external-ids).

## Installation

* Local

```bash
pip install --upgrade .
pip show bundlebuilder
```

* GitHub

```bash
pip install --upgrade git+https://github.com/CiscoSecurity/tr-05-ctim-bundle-builder.git[@branch_name_or_release_version]
pip show bundlebuilder
```

* PyPi

```bash
pip install --upgrade bundlebuilder[==release_version]
pip show bundlebuilder
```

## Usage

Here is a bit extended version of the adapted
[example](https://github.com/threatgrid/ctim/blob/master/doc/tutorials/modeling-threat-intel-ctim.md#173-example-bundle)
showing how to properly use BB along with its available models and their APIs:

```python
import json

from bundlebuilder.models.entity import BaseEntity
from bundlebuilder.models.primary import (
    Bundle,
    Sighting,
    Judgement,
    Indicator,
    Relationship,
    Verdict,
)
from bundlebuilder.models.secondary import (
    ObservedTime,
    Observable,
    ValidTime,
)
from bundlebuilder.session import Session


def print_json(entity: BaseEntity):
    print(json.dumps(entity.json, indent=2))


def main():
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

    print_json(bundle)


if __name__ == '__main__':
    main()
```
