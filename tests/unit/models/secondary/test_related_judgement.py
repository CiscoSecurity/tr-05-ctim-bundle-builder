from pytest import raises as assert_raises

from bundlebuilder.constants import CONFIDENCE_CHOICES
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import RelatedJudgement


def test_related_judgement_validation_fails():
    related_judgement_data = {
        'confidence': 'Unbelievable',
    }

    with assert_raises(ValidationError) as exc_info:
        RelatedJudgement(**related_judgement_data)

    error = exc_info.value

    assert error.args == ({
        'judgement_id': ['Missing data for required field.'],
        'confidence': [
            f'Must be one of: {", ".join(map(repr, CONFIDENCE_CHOICES))}.'
        ],
    },)


def test_related_judgement_validation_succeeds():
    related_judgement_data = {
        'judgement_id': 'transient:prefix-judgement-uuid',
        'confidence': 'Low',
        'relationship': 'related-to',
        'source': 'CTIM Bundle Builder',
    }

    related_judgement = RelatedJudgement(**related_judgement_data)

    assert related_judgement.json == related_judgement_data
