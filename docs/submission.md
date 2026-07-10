# Scratch Wallet

**Builder:** Mathieu D. WEILL  
**Track:** AI / DeFi  
**Chain:** HashKey Chain  
**Tagline:** A lottery ticket that knows when not to play.

## One-liner

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet that hunts for small on-chain opportunities while protecting users from unsafe trades, claims, and approvals.

## Problem

Autonomous trading bots are dangerous for normal users. They often encourage users to connect valuable wallets, overtrade, ignore gas and slippage, and expose assets through unsafe approvals. Small-wallet DeFi also has a different reality: users chase micro-opportunities, claims, incentives, and route edges, but one bad signature can cost far more than the opportunity is worth.

## Solution

Scratch Wallet isolates the risk. Users fund a tiny dedicated wallet, choose a risk mode, and let the agent scan for small opportunities. The agent simulates every action, checks gas, slippage, liquidity, token allowlists, approval risk, and bankroll limits. It rejects most opportunities and stops automatically when loss limits are reached.

## Why HashKey Chain

HashKey Chain is used as the execution and audit layer. Scratch Wallet can anchor every played opportunity, skipped opportunity, blocked rug, and stop event through `ScratchWalletRegistry.sol`. This creates a transparent trail for autonomous agent decisions.

## Why AI

AI is used as an explanation layer for autonomous execution. It turns technical decisions into plain English: why the agent played, why it skipped, why a claim was blocked, and why the wallet stopped.

## What is built

- Streamlit MVP deployable on Streamlit Community Cloud
- deterministic scratch engine
- opportunity scanner
- trade simulator
- bankroll guard
- Claim Shield
- P&L dashboard
- report hashing
- mock and real HashKey anchor flow
- Solidity decision registry
- Hardhat deployment scripts

## Safety design

- no main wallet connection
- tiny isolated wallet only
- hard max trade size
- hard daily loss limit
- hard drawdown limit
- unsafe approvals blocked
- dry-run first
- no custody
- no yield promise

## Demo flow

1. Create a Scratch Wallet with 100 USDC simulated bankroll.
2. Choose Normal Mode.
3. Run Scratch Today.
4. Show skipped opportunities and one tiny simulated play.
5. Show Claim Shield blocking a fake airdrop.
6. Generate report hash.
7. Anchor the decision report on HashKey Chain.

## Future roadmap

- live HashKey DEX quote adapters
- burner wallet creation
- Telegram bot alerts
- browser extension for Claim Shield
- strategy marketplace
- premium simulation mode
- optional performance-fee vaults with explicit user control
