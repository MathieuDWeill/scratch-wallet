from .models import WalletState, DecisionLog


def daily_summary(wallet: WalletState, logs: list[DecisionLog]) -> str:
    played = sum(1 for log in logs if log.decision == "PLAY")
    skipped = sum(1 for log in logs if log.decision == "SKIP")
    pnl_pct = (wallet.current_bankroll - wallet.starting_bankroll) / wallet.starting_bankroll * 100
    if wallet.stopped:
        mood = "Stopped. Goblin goes back in the box."
    elif wallet.realized_pnl > 0:
        mood = "Still poor, but alive."
    else:
        mood = "No heroic trade. Survival is alpha."
    return (
        f"Scratch result: scanned {len(logs)} opportunities, played {played}, skipped {skipped}, "
        f"dodged {wallet.rugs_dodged} rug-shaped object(s). Net P&L: {wallet.realized_pnl:+.4f} USDC "
        f"({pnl_pct:+.2f}%). Bot mood: {mood}"
    )


def roast_for_log(log: DecisionLog) -> str:
    if log.decision == "PLAY":
        return "Played: tiny edge survived the spreadsheet of doom. Not financial advice, just goblin arithmetic."
    if "Rug dodged" in log.reason:
        return "Skipped: this was not free money, it was a wallet drainer wearing a party hat."
    if "slippage" in log.reason.lower():
        return "Skipped: the edge died of slippage before it reached adulthood."
    if "liquidity" in log.reason.lower():
        return "Skipped: liquidity was thinner than the plot of a fake airdrop."
    return "Skipped: rejected opportunities are a feature, not a bug."
