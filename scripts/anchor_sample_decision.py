from engine.chain_anchor import anchor_decision_real, mock_anchor

if __name__ == "__main__":
    result = anchor_decision_real(
        opportunity_id="demo-usdc-hsk-usdt",
        decision="PLAY",
        risk_mode="Normal",
        starting_bankroll=100.0,
        trade_size=8.0,
        gross_edge_bps=44,
        net_edge_bps=12,
        risk_score=24,
        played=True,
        report_hash="0x" + "11" * 32,
        report_uri="",
    )
    if not result.ok:
        print("Real anchor unavailable:", result.message)
        print(mock_anchor("0x" + "11" * 32))
    else:
        print(result)
