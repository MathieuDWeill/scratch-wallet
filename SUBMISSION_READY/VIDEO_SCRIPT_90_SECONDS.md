# 90-second demo video script

## 0–10s — Hook
“Most autonomous trading bots ask users to connect a valuable wallet. Scratch Wallet does the opposite: it starts with a tiny isolated wallet and hard loss limits.”

Show landing page: **Scratch Wallet — A lottery ticket that knows when not to play.**

## 10–25s — Setup
Set bankroll to `100 USDC`. Select `Normal Mode`.

Say:
“Users pick a bankroll and risk mode. The agent can only operate inside that tiny wallet.”

## 25–45s — Run agent
Click **Scratch Today**.

Say:
“The agent scans opportunities, simulates execution costs, gas, slippage and safety buffers, then rejects most candidates.”

Show metrics: played, skipped, rugs dodged, P&L.

## 45–65s — Show journal
Scroll through Scratch Journal.

Say:
“Each decision is explainable. It plays tiny edges that survive the risk model, skips weak trades, and blocks fake claims or unsafe approvals.”

Highlight fake airdrop blocked.

## 65–80s — Anchor
Click **Mock Anchor** or **Real HashKey Anchor** if configured.

Say:
“Each decision report can be anchored on HashKey Chain through ScratchWalletRegistry, creating an audit trail for autonomous-agent behavior.”

## 80–90s — Close
Say:
“Scratch Wallet does not promise to beat the market. It makes autonomous DeFi exploration bounded, explainable, and auditable.”


## Automated recording

Run this to create the demo video automatically:

```bash
./scripts/record_demo.sh
```

Or on Windows:

```powershell
scripts\record_demo.ps1
```

Upload the generated `scratch_wallet_demo.mp4` from `demo_recordings/scratch-wallet-demo-*/`.
