from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    SensorCoordinates,
    Observable,
)


def test_sensor_coordinates_validation_fails():
    sensor_coordinates_data = {
        'location': 'Europe',
        'observables': [object()],
    }

    with assert_raises(ValidationError) as exc_info:
        SensorCoordinates(**sensor_coordinates_data)

    error = exc_info.value

    assert error.args == ({
        'location': ['Unknown field.'],
        'observables': {
            0: ['Not a valid CTIM Observable.'],
        },
        'type': ['Missing data for required field.'],
    },)


def test_sensor_coordinates_validation_succeeds():
    observable = Observable(
        type='device',
        value='centos',
    )

    sensor_coordinates_data = {
        'observables': [observable],
        'type': 'network.gateway',
        'os': 'linux',
    }

    sensor_coordinates = SensorCoordinates(**sensor_coordinates_data)

    sensor_coordinates_data['observables'] = [observable.json]

    assert sensor_coordinates.json == sensor_coordinates_data
