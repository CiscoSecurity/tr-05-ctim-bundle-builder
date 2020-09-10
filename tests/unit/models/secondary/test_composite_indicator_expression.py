from pytest import raises as assert_raises

from bundlebuilder.constants import BOOLEAN_OPERATOR_CHOICES
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import CompositeIndicatorExpression


def test_composite_indicator_expression_validation_fails():
    composite_indicator_expression_data = {
        'operator': 'xor',
    }

    with assert_raises(ValidationError) as exc_info:
        CompositeIndicatorExpression(**composite_indicator_expression_data)

    error = exc_info.value

    assert error.args == ({
        'indicator_ids': ['Missing data for required field.'],
        'operator': [
            'Must be one of: '
            f'{", ".join(map(repr, BOOLEAN_OPERATOR_CHOICES))}.'
        ],
    },)


def test_composite_indicator_expression_validation_succeeds():
    composite_indicator_expression_data = {
        'indicator_ids': ['123', '456', '789'],
        'operator': 'and',
    }

    composite_indicator_expression = CompositeIndicatorExpression(
        **composite_indicator_expression_data
    )

    assert composite_indicator_expression.json == (
        composite_indicator_expression_data
    )
