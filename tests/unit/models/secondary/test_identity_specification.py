from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    IdentitySpecification,
    Observable,
    ObservedTime,
)
from tests.unit.utils import utc_now_iso


def test_identity_specification_validation_fails():
    identity_specification_data = {
        'local': True,
        'observables': [object()],
        'observed_time': object(),
    }

    with assert_raises(ValidationError) as exc_info:
        IdentitySpecification(**identity_specification_data)

    error = exc_info.value

    assert error.args == ({
        'local': ['Unknown field.'],
        'observables': {
            0: ['Not a valid CTIM Observable.'],
        },
        'observed_time': ['Not a valid CTIM ObservedTime.'],
        'type': ['Missing data for required field.'],
    },)


def test_identity_specification_validation_succeeds():
    observable = Observable(
        type='device',
        value='macos',
    )

    observed_time = ObservedTime(
        start_time=utc_now_iso(),
    )

    identity_specification_data = {
        'observables': [observable],
        'observed_time': observed_time,
        'type': 'endpoint.workstation',
        'os': 'darwin',
    }

    identity_specification = IdentitySpecification(
        **identity_specification_data
    )

    identity_specification_data['observables'] = [observable.json]
    identity_specification_data['observed_time'] = observed_time.json

    assert identity_specification.json == identity_specification_data
