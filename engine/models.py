from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

RiskModeName = Literal["Chicken", "Normal", "Degen"]
OpportunityType = Literal[
    "stablecoin_route",
    "dex_route",
    "pool_imbalance",
    "incentive",
    "safe_claim",
    "suspicious_claim",
    "high_apy_trap",
]
Decision = Literal["PLAY", "SKIP", "STOP"]

@dataclass(frozen=True)
class RiskMode:
    name: RiskModeName
    max_trade_pct: float
    max_daily_loss_pct: float
    max_total_drawdown_pct: float
    min_net_edge_bps: int
    max_slippage_bps: int
    min_liquidity_usd: float
    allowed_tokens: tuple[str, ...]
    allowed_types: tuple[OpportunityType, ...]
    claim_farming: bool

@dataclass(frozen=True)
class Opportunity:
    id: str
    title: str
    kind: OpportunityType
    route: tuple[str, ...]
    protocol: str
    capital_required_usd: float
    gross_edge_bps: int
    estimated_gas_usd: float
    estimated_slippage_bps: int
    liquidity_usd: float
    risk_score: int
    confidence: int
    description: str
    red_flags: tuple[str, ...] = ()
    green_flags: tuple[str, ...] = ()
    approval_request: str | None = None
    verified_contract: bool = True

@dataclass
class Simulation:
    opportunity: Opportunity
    trade_size_usd: float
    gross_profit_usd: float
    gas_usd: float
    slippage_cost_usd: float
    safety_buffer_usd: float
    net_profit_usd: float
    net_edge_bps: int
    recommendation: Decision
    reasons: list[str] = field(default_factory=list)

@dataclass
class WalletState:
    starting_bankroll: float
    current_bankroll: float
    risk_mode: RiskMode
    daily_loss: float = 0.0
    realized_pnl: float = 0.0
    trades_played: int = 0
    opportunities_skipped: int = 0
    rugs_dodged: int = 0
    stopped: bool = False

@dataclass
class DecisionLog:
    opportunity_id: str
    title: str
    decision: Decision
    net_edge_bps: int
    risk_score: int
    trade_size_usd: float
    pnl_usd: float
    reason: str
    tx_hash: str | None = None
