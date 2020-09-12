from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import ThreatBrainSpecification


def test_threat_brain_specification_validation_fails():
    threat_brain_specification_data = {}

    with assert_raises(ValidationError) as exc_info:
        ThreatBrainSpecification(**threat_brain_specification_data)

    error = exc_info.value

    assert error.args == ({
        'variables': ['Missing data for required field.'],
    },)


def test_threat_brain_specification_validation_succeeds():
    threat_brain_specification_data = {
        'variables': ['x', 'y', 'z'],
        'query': 'sum(x, y, z)',
    }

    threat_brain_specification = ThreatBrainSpecification(
        **threat_brain_specification_data
    )

    threat_brain_specification_data['type'] = 'ThreatBrain'

    assert threat_brain_specification.json == threat_brain_specification_data
