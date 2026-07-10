from engine.models import WalletState
from engine.risk_modes import RISK_MODES
from engine.scratch_engine import run_daily_scratch
from engine.claim_shield import inspect_claim
from engine.mock_data import OPPORTUNITIES


def test_daily_scratch_generates_decisions():
    wallet = WalletState(starting_bankroll=100, current_bankroll=100, risk_mode=RISK_MODES["Normal"])
    wallet, logs, simulations = run_daily_scratch(wallet)
    assert logs
    assert simulations
    assert wallet.current_bankroll >= 0


def test_fake_airdrop_is_blocked():
    fake = next(o for o in OPPORTUNITIES if o.id == "op-fake-airdrop")
    result = inspect_claim(fake)
    assert result["safe"] is False
    assert result["risk"] == "CRITICAL"
