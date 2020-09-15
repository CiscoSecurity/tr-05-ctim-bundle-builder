from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    ObservedRelation,
    Observable,
)


def test_observed_relation_validation_fails():
    observed_relation_data = {
        'score': 4.61,
        'related': object(),
        'relation': 'Is_Fond_Of',
        'source': object(),
        'relation_info': {
            'bool': False,
            'int': 1,
            'str': 'two',
        },
    }

    with assert_raises(ValidationError) as exc_info:
        ObservedRelation(**observed_relation_data)

    error = exc_info.value

    assert error.args == ({
        'score': ['Unknown field.'],
        'origin': ['Missing data for required field.'],
        'related': ['Not a valid CTIM Observable.'],
        'source': ['Not a valid CTIM Observable.'],
    },)


def test_observed_relation_validation_succeeds():
    related = Observable(
        type='url',
        value='https://fake.org/good.html',
    )
    source = Observable(
        type='url',
        value='https://fake.org/bad.html',
    )

    observed_relation_data = {
        'origin': 'A bad URL redirecting to a good one.',
        'related': related,
        'relation': 'Redirects_To',
        'source': source,
    }

    observed_relation = ObservedRelation(**observed_relation_data)

    observed_relation_data['related'] = related.json
    observed_relation_data['source'] = source.json

    assert observed_relation.json == observed_relation_data
