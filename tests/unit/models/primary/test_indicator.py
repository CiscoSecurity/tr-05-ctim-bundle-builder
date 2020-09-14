from pytest import raises as assert_raises

from bundlebuilder.constants import (
    CONFIDENCE_CHOICES,
    DESCRIPTION_MAX_LENGTH,
    INDICATOR_TYPE_CHOICES,
    LIKELY_IMPACT_MAX_LENGTH,
    TEST_MECHANISM_MAX_LENGTH,
    REVISION_MIN_VALUE,
    SEVERITY_CHOICES,
    SHORT_DESCRIPTION_LENGTH,
    TLP_CHOICES,
    SCHEMA_VERSION,
    DEFAULT_SESSION_SOURCE,
    DEFAULT_SESSION_SOURCE_URI,
    DEFAULT_SESSION_EXTERNAL_ID_PREFIX,
)
from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import (
    Indicator,
    ValidTime,
    CompositeIndicatorExpression,
    KillChainPhase,
    JudgementSpecification,
    ThreatBrainSpecification,
    SnortSpecification,
    SIOCSpecification,
    OpenIOCSpecification,
    RelatedJudgement,
)
from tests.unit.utils import (
    mock_transient_id,
    mock_external_id,
    utc_now_iso,
)


def test_indicator_validation_fails():
    indicator_data = {
        'greeting': '¡Hola!',
        'valid_time': object(),
        'composite_indicator_expression': object(),
        'confidence': 'Unbelievable',
        'description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'external_references': [object()],
        'indicator_type': ['Californication', 'Anonymization', 'Exfiltration'],
        'kill_chain_phases': [object()],
        'language': 'Python',
        'likely_impact': '\U0001f4a9' * (LIKELY_IMPACT_MAX_LENGTH + 1),
        'negate': 69,
        'revision': -273,
        'severity': 'Insignificant',
        'short_description': '\U0001f4a9' * DESCRIPTION_MAX_LENGTH,
        'specification': object(),
        'test_mechanisms': ['\U0001f4a9' * (TEST_MECHANISM_MAX_LENGTH + 1)],
        'timestamp': '4:20',
        'title': 'OMG! The Best CTIM Bundle Builder Ever!',
        'tlp': 'razzmatazz',
    }

    with assert_raises(ValidationError) as exc_info:
        Indicator(**indicator_data)

    error = exc_info.value

    assert error.args == ({
        'greeting': ['Unknown field.'],
        'producer': ['Missing data for required field.'],
        'valid_time': ['Not a valid CTIM ValidTime.'],
        'composite_indicator_expression': [
            'Not a valid CTIM CompositeIndicatorExpression.'
        ],
        'confidence': [
            f'Must be one of: {", ".join(map(repr, CONFIDENCE_CHOICES))}.'
        ],
        'external_references': {
            0: ['Not a valid CTIM ExternalReference.'],
        },
        'indicator_type': {
            0: [
                'Must be one of: '
                f'{", ".join(map(repr, INDICATOR_TYPE_CHOICES))}.'
            ],
        },
        'kill_chain_phases': {
            0: ['Not a valid CTIM KillChainPhase.'],
        },
        'likely_impact': [
            f'Must be at most {LIKELY_IMPACT_MAX_LENGTH} characters long.'
        ],
        'negate': ['Not a valid boolean.'],
        'revision': [
            f'Must be greater than or equal to {REVISION_MIN_VALUE}.'
        ],
        'severity': [
            f'Must be one of: {", ".join(map(repr, SEVERITY_CHOICES))}.'
        ],
        'short_description': [
            f'Must be at most {SHORT_DESCRIPTION_LENGTH} characters long.'
        ],
        'specification': [
            'Not a valid CTIM JudgementSpecification.',
            'Not a valid CTIM ThreatBrainSpecification.',
            'Not a valid CTIM SnortSpecification.',
            'Not a valid CTIM SIOCSpecification.',
            'Not a valid CTIM OpenIOCSpecification.',
        ],
        'test_mechanisms': {
            0: [
                f'Must be at most {TEST_MECHANISM_MAX_LENGTH} characters long.'
            ],
        },
        'timestamp': ['Not a valid datetime.'],
        'tlp': [
            f'Must be one of: {", ".join(map(repr, TLP_CHOICES))}.'
        ],
    },)


def test_indicator_validation_succeeds():
    valid_time = ValidTime(
        start_time=utc_now_iso(),
        end_time=utc_now_iso(),
    )

    composite_indicator_expression = CompositeIndicatorExpression(
        indicator_ids=['123', '456', '789'],
        operator='and',
    )

    kill_chain_phase = KillChainPhase(
        kill_chain_name=' - Kill - Chain - Name - ',
        phase_name=' _ Phase _ Name _ ',
    )

    specifications = [
        JudgementSpecification(
            judgements=['judgement'],
            required_judgements=[
                RelatedJudgement(
                    judgement_id='judgement_id',
                ),
            ],
        ),
        ThreatBrainSpecification(
            variables=['variable'],
            query='query',
        ),
        SnortSpecification(
            snort_sig='snort_sig',
        ),
        SIOCSpecification(
            SIOC='SIOC',
        ),
        OpenIOCSpecification(
            open_IOC='open_IOC',
        ),
    ]

    for specification in specifications:
        indicator_data = {
            'producer': 'SoftServe',
            'confidence': 'High',
            'valid_time': valid_time,
            'composite_indicator_expression': composite_indicator_expression,
            'indicator_type': ['File Hash Watchlist'],
            'kill_chain_phases': [kill_chain_phase],
            'negate': True,
            'revision': 0,
            'severity': 'High',
            'specification': specification,
            'tags': ['ctim', 'bundle', 'builder'],
            'timestamp': utc_now_iso(),
            'tlp': 'red',
        }

        indicator = Indicator(**indicator_data)

        indicator_data['valid_time'] = valid_time.json
        indicator_data['composite_indicator_expression'] = (
            composite_indicator_expression.json
        )
        indicator_data['kill_chain_phases'] = [{
            'kill_chain_name': 'kill-chain-name',
            'phase_name': 'phase-name',
        }]
        indicator_data['specification'] = specification.json

        type_ = 'indicator'

        assert indicator.json == {
            'type': type_,
            'schema_version': SCHEMA_VERSION,
            'source': DEFAULT_SESSION_SOURCE,
            'source_uri': DEFAULT_SESSION_SOURCE_URI,
            'id': mock_transient_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_),
            'external_ids': [
                mock_external_id(DEFAULT_SESSION_EXTERNAL_ID_PREFIX, type_)
            ],
            **indicator_data
        }
