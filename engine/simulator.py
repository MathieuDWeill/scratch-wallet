from .models import Opportunity, Simulation, WalletState


def simulate(opportunity: Opportunity, wallet: WalletState) -> Simulation:
    mode = wallet.risk_mode
    max_trade = wallet.current_bankroll * mode.max_trade_pct
    trade_size = min(max_trade, max(opportunity.capital_required_usd, 0.0))
    if opportunity.kind == "safe_claim":
        trade_size = 0.0
    if trade_size == 0 and opportunity.kind not in ("safe_claim", "suspicious_claim"):
        trade_size = max_trade

    gross_profit = trade_size * opportunity.gross_edge_bps / 10_000
    slippage_cost = trade_size * opportunity.estimated_slippage_bps / 10_000
    safety_buffer = trade_size * 0.0015
    gas = opportunity.estimated_gas_usd
    if opportunity.kind == "safe_claim":
        gross_profit = 0.35  # mock claim reward net before gas
        safety_buffer = 0.02
    net_profit = gross_profit - gas - slippage_cost - safety_buffer
    net_edge_bps = int((net_profit / trade_size) * 10_000) if trade_size > 0 else int(net_profit * 100)

    reasons: list[str] = []
    recommendation = "PLAY"
    if opportunity.kind not in mode.allowed_types:
        recommendation = "SKIP"
        reasons.append(f"{opportunity.kind} is not allowed in {mode.name} mode.")
    if any(token not in mode.allowed_tokens and token not in ("CLAIM", "UNKNOWN", "NEWCOIN") for token in opportunity.route):
        recommendation = "SKIP"
        reasons.append("Route includes a token outside the allowlist.")
    if opportunity.estimated_slippage_bps > mode.max_slippage_bps:
        recommendation = "SKIP"
        reasons.append("Slippage exceeds the selected risk mode limit.")
    if opportunity.liquidity_usd and opportunity.liquidity_usd < mode.min_liquidity_usd:
        recommendation = "SKIP"
        reasons.append("Liquidity is too thin for this mode.")
    if not opportunity.verified_contract:
        recommendation = "SKIP"
        reasons.append("Contract is not verified or not trusted.")
    if opportunity.approval_request:
        recommendation = "SKIP"
        reasons.append("Unsafe approval detected by Claim Shield.")
    if net_edge_bps < mode.min_net_edge_bps and opportunity.kind != "safe_claim":
        recommendation = "SKIP"
        reasons.append("Net edge does not survive gas, slippage, and safety buffer.")
    if wallet.daily_loss >= wallet.starting_bankroll * mode.max_daily_loss_pct:
        recommendation = "STOP"
        reasons.append("Daily loss limit already reached.")

    if not reasons:
        reasons.append("Net edge survived risk checks for the selected mode.")
    return Simulation(opportunity, trade_size, gross_profit, gas, slippage_cost, safety_buffer, net_profit, net_edge_bps, recommendation, reasons)
