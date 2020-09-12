from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    JudgementSpecification,
    RelatedJudgement,
)


def test_judgement_specification_validation_fails():
    judgement_specification_data = {}

    with assert_raises(ValidationError) as exc_info:
        JudgementSpecification(**judgement_specification_data)

    error = exc_info.value

    assert error.args == ({
        'judgements': ['Missing data for required field.'],
        'required_judgements': ['Missing data for required field.'],
    },)


def test_judgement_specification_validation_succeeds():
    required_judgement = RelatedJudgement(
        judgement_id='judgement_id',
    )

    judgement_specification_data = {
        'judgements': ['judgement'],
        'required_judgements': [required_judgement],
    }

    judgement_specification = JudgementSpecification(
        **judgement_specification_data
    )

    judgement_specification_data['required_judgements'] = [
        required_judgement.json
    ]
    judgement_specification_data['type'] = 'Judgement'

    assert judgement_specification.json == judgement_specification_data
