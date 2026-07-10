# DoraHacks Submission — Scratch Wallet

## Project name
Scratch Wallet

## Builder
Mathieu D. WEILL

## Track
AI / DeFi

## One-liner
Scratch Wallet is a risk-capped autonomous DeFi micro-wallet that hunts for small on-chain opportunities while protecting users from unsafe trades, claims, and approvals.

## Short description
Scratch Wallet gives users a bounded way to explore autonomous DeFi. Instead of connecting a main wallet to a trading bot, users fund a tiny isolated wallet, choose a risk mode, and let the agent scan for route edges, pool imbalances, incentives, and safe claims.

Every opportunity is simulated before execution. Dangerous approvals are blocked. Most opportunities are rejected. The wallet stops automatically when predefined loss limits are reached. Decisions can be anchored on HashKey Chain for transparency.

## Long description
Small-wallet DeFi often feels like scratching a lottery ticket: users chase small opportunities, claims, incentives, and route edges, but the downside can become catastrophic when they connect their main wallet or sign unsafe approvals.

Scratch Wallet changes the default. Users do not connect their main wallet. They fund a tiny isolated wallet, define hard risk limits, and let an autonomous agent hunt only inside that bounded bankroll.

The agent scans mock HashKey Chain opportunities, simulates each action, estimates gas, slippage and safety buffers, applies a bankroll guard, blocks dangerous claim approvals, and produces a clear decision journal. Each played opportunity, skipped opportunity, rug dodge, or stop event can be anchored through `ScratchWalletRegistry` on HashKey Chain.

The product does not promise guaranteed returns. Its thesis is that autonomous finance should start with bounded downside.

## Tagline
A lottery ticket that knows when not to play.

## Problem
Autonomous trading bots are dangerous for ordinary users because they often require access to valuable wallets, overtrade, ignore execution costs, and expose users to unsafe approvals or wallet-drainer patterns.

## Solution
Scratch Wallet isolates risk inside a tiny dedicated wallet. The agent uses hard risk modes, simulates each opportunity, rejects unsafe actions, explains every decision, and stops automatically when loss limits are hit.

## Why HashKey Chain
HashKey Chain is used as the execution and audit layer. Scratch Wallet anchors autonomous-agent decisions through a smart contract so users and reviewers can verify what the agent played, skipped, blocked, or stopped.

## Why AI
AI is used as the decision explanation layer: it turns technical trade and claim outcomes into plain-English summaries that users can understand. The MVP currently uses deterministic engines for safety and reliability, with an AI-style narrator layer for transparent explanations.

## Technical implementation
- Streamlit frontend for fast free deployment.
- Python autonomous scratch engine.
- Opportunity scanner with mock HashKey DeFi opportunities.
- Trade simulator for edge, gas, slippage, safety buffer, and net expected result.
- Bankroll guard with Chicken, Normal, and Degen risk modes.
- Claim Shield module for dangerous approvals and fake claims.
- Solidity registry contract for decision anchoring.
- Hardhat deployment scripts for HashKey Chain.
- Web3.py integration for real HashKey anchor transactions from Streamlit.

## Smart contract
`ScratchWalletRegistry.sol` anchors:
- scratch wallet address;
- opportunity hash;
- decision type;
- risk mode;
- starting bankroll;
- trade size;
- gross and net edge;
- risk score;
- played/skipped status;
- report hash;
- report URI.

HashKey Chain mainnet deployment:

- Contract address: `0x33145C082811c5E88ce055DAD816aE540a89da94`
- Contract explorer: https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94
- Anchor transaction: https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6
- Funding transaction: https://hashkey.blockscout.com/tx/0x88262d336419b7592cf0582fb2aed823ce9c15033aab8a286c70f7195a2f96d4

## Demo flow
1. Open the Streamlit app.
2. Select bankroll and risk mode.
3. Click “Scratch Today”.
4. Watch the agent scan opportunities.
5. Review played, skipped, rug-dodged, and stopped decisions.
6. Download the report JSON.
7. Anchor the report using Mock Anchor or Real HashKey Anchor.

## Links
- Live demo: TODO
- GitHub repo: https://github.com/MathieuDWeill/scratch-wallet
- Demo video: TODO
- HashKey contract: https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94
- Example transaction: https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6

## Disclaimer
Scratch Wallet is a hackathon MVP. It is not financial advice, does not guarantee profit, and should only ever be used with tiny isolated wallets and funds users can afford to lose.


## Logo

Use `SUBMISSION_READY/scratch-wallet-logo-480.png` as the DoraHacks BUIDL logo. It is 480×480 PNG and under 2 MB.
