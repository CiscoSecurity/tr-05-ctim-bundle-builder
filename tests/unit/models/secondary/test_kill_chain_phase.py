from pytest import raises as assert_raises

from bundlebuilder.exceptions import ValidationError
from bundlebuilder.models import KillChainPhase


def test_kill_chain_phase_validation_fails():
    kill_chain_phase_data = {
        'algorithm_name': 'divide-and-conquer',
    }

    with assert_raises(ValidationError) as exc_info:
        KillChainPhase(**kill_chain_phase_data)

    error = exc_info.value

    assert error.args == ({
        'algorithm_name': ['Unknown field.'],
        'kill_chain_name': ['Missing data for required field.'],
        'phase_name': ['Missing data for required field.'],
    },)


def test_kill_chain_phase_validation_succeeds():
    kill_chain_phase_data = {
        'kill_chain_name': ' - Kill - Chain - Name - ',
        'phase_name': ' _ Phase _ Name _ ',
    }

    kill_chain_phase = KillChainPhase(**kill_chain_phase_data)

    kill_chain_phase_data = {
        'kill_chain_name': 'kill-chain-name',
        'phase_name': 'phase-name',
    }

    assert kill_chain_phase.json == kill_chain_phase_data
