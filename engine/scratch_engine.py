from __future__ import annotations
import hashlib
from .models import WalletState, DecisionLog
from .mock_data import OPPORTUNITIES
from .simulator import simulate
from .claim_shield import inspect_claim


def short_hash(text: str) -> str:
    return "0x" + hashlib.sha256(text.encode()).hexdigest()[:16]


def run_daily_scratch(wallet: WalletState) -> tuple[WalletState, list[DecisionLog], list]:
    logs: list[DecisionLog] = []
    simulations = []
    for op in sorted(OPPORTUNITIES, key=lambda o: (o.risk_score, -o.gross_edge_bps)):
        if wallet.stopped:
            break
        sim = simulate(op, wallet)
        simulations.append(sim)
        claim = inspect_claim(op) if "claim" in op.kind else None
        if claim and not claim["safe"]:
            wallet.opportunities_skipped += 1
            wallet.rugs_dodged += 1
            logs.append(DecisionLog(op.id, op.title, "SKIP", sim.net_edge_bps, op.risk_score, 0, 0, "Rug dodged: " + claim["finding"], short_hash(op.id + "rug")))
            continue
        if sim.recommendation == "PLAY":
            pnl = round(sim.net_profit_usd, 4)
            wallet.current_bankroll += pnl
            wallet.realized_pnl += pnl
            if pnl < 0:
                wallet.daily_loss += abs(pnl)
            wallet.trades_played += 1
            logs.append(DecisionLog(op.id, op.title, "PLAY", sim.net_edge_bps, op.risk_score, sim.trade_size_usd, pnl, sim.reasons[0], short_hash(op.id + "play")))
        elif sim.recommendation == "STOP":
            wallet.stopped = True
            logs.append(DecisionLog(op.id, op.title, "STOP", sim.net_edge_bps, op.risk_score, sim.trade_size_usd, 0, "; ".join(sim.reasons), short_hash(op.id + "stop")))
        else:
            wallet.opportunities_skipped += 1
            logs.append(DecisionLog(op.id, op.title, "SKIP", sim.net_edge_bps, op.risk_score, sim.trade_size_usd, 0, "; ".join(sim.reasons), short_hash(op.id + "skip")))
        if wallet.daily_loss >= wallet.starting_bankroll * wallet.risk_mode.max_daily_loss_pct:
            wallet.stopped = True
    return wallet, logs, simulations
