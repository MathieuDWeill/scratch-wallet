# Scratch Wallet

**A lottery ticket that knows when not to play.**

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet built by Mathieu D. WEILL for the HashKey Chain On-Chain Horizon Hackathon.

Users fund a tiny isolated wallet instead of connecting their main wallet. The agent then scans HashKey Chain-style opportunities, simulates every action, blocks unsafe approvals, rejects most opportunities, and stops automatically when predefined loss limits are reached.

The MVP includes:

- Streamlit app;
- autonomous scratch engine;
- risk modes: Chicken, Normal, Degen;
- opportunity scanner;
- trade simulator;
- bankroll guard;
- Claim Shield;
- decision journal;
- report JSON download;
- Solidity decision registry;
- HashKey Chain deployment scripts;
- real or mock report anchoring.

## Run locally

```bash
pip install -r requirements.txt
python scripts/preflight.py
streamlit run app.py
```

## Deploy contract

```bash
npm install
npm run compile
npm run test
cp .env.example .env
npm run deploy:hashkey
```

## Product thesis

Autonomous finance should start with bounded downside.
