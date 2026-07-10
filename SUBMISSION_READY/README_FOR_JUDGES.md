# Scratch Wallet — Judge README

**Builder:** Mathieu D. WEILL  
**Track:** AI / DeFi  
**Chain:** HashKey Chain  
**Tagline:** A lottery ticket that knows when not to play.

## 30-second explanation

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet. Users do not connect their main wallet. They fund a tiny isolated wallet, pick a risk mode, and let the agent scan for small on-chain opportunities. The agent simulates every action, blocks dangerous approvals, rejects most opportunities, and stops automatically at hard loss limits.

## What is implemented

- Streamlit demo app.
- Deterministic autonomous scratch engine.
- Risk modes: Chicken / Normal / Degen.
- Opportunity scanner with mock HashKey-style DeFi opportunities.
- Trade simulation with gross edge, slippage, gas buffer, and net edge.
- Claim Shield for unsafe approvals and fake airdrops.
- Shareable Scratch Card.
- HashKey anchor plumbing.
- Solidity registry contract.
- Playwright + ffmpeg automated demo video pipeline.
- Copy/paste DoraHacks submission pack.

## HashKey mainnet proof

- Contract address: `0x33145C082811c5E88ce055DAD816aE540a89da94`
- Contract explorer: https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94
- Anchor transaction: https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6
- Funding transaction: https://hashkey.blockscout.com/tx/0x88262d336419b7592cf0582fb2aed823ce9c15033aab8a286c70f7195a2f96d4

## Why this is different

Most autonomous agents optimize for aggression. Scratch Wallet optimizes for survivability. It accepts that small-wallet DeFi often feels like a lottery ticket, then makes the ticket safer: bounded bankroll, hard stop-loss, scam protection, and auditable decisions.

## Demo path

1. Open the app.
2. Click **Scratch Today**.
3. Watch the agent scan, play, skip, and block a rug.
4. Open **Scratch Card** for the shareable result.
5. Open **Claim Shield** to see fake airdrop detection.
6. Open **Anchor / Deploy** to see the HashKey configuration.
