# Scratch Wallet

**Builder:** Mathieu D. WEILL  
**Hackathon:** HashKey Chain On-Chain Horizon Hackathon  
**Tagline:** *A lottery ticket that knows when not to play.*

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet. Users do **not** connect their main wallet. They fund a tiny isolated wallet, choose a risk mode, and let the agent scan for small on-chain opportunities such as route edges, pool imbalances, incentives, and safe claims.

The agent simulates every action, blocks dangerous approvals, rejects most opportunities, and stops automatically when loss limits are reached. Decisions can be anchored on HashKey Chain through `ScratchWalletRegistry.sol`.

## Why this exists

Autonomous trading bots are usually framed as smart-money machines. Scratch Wallet assumes the honest opposite: small-wallet DeFi often feels like scratching a lottery ticket. The product makes that experience bounded, explainable, and auditable.

**Core principle:** autonomous finance should start with bounded downside.

## Submission links

- GitHub: `https://github.com/MathieuDWeill/scratch-wallet`
- Demo video: `https://youtu.be/-zdwef1rJs4`
- HashKey mainnet contract: `https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94`
- Anchor transaction: `https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6`

## What is already built

- Streamlit Community Cloud-ready app (`app.py`)
- deterministic autonomous scratch engine
- risk modes: Chicken, Normal, Degen
- opportunity scanner with realistic mock market data
- trade simulator with gas/slippage/safety-buffer checks
- Claim Shield for unsafe approvals and fake claim flows
- P&L dashboard and Scratch Journal
- real/mock HashKey report anchoring flow
- Solidity registry contract
- Hardhat deployment config for HashKey Chain
- deployment scripts and docs
- hackathon submission copy

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy the app on Streamlit Community Cloud

1. Push this folder to a GitHub repo.
2. Create a new app on Streamlit Community Cloud.
3. Main file: `app.py`.
4. Add secrets only after the contract is deployed.

Example secrets:

```toml
HASHKEY_RPC_URL = "https://mainnet.hsk.xyz"
HASHKEY_CHAIN_ID = "177"
SCRATCH_REGISTRY_ADDRESS = "0x..."
SCRATCH_WALLET_ADDRESS = "0x..."
ANCHOR_PRIVATE_KEY = "0x..."
```

Use a fresh burner wallet with tiny HSK only. Never use your main wallet private key.

## HashKey Chain deployment

Network parameters used by this repo:

- RPC: `https://mainnet.hsk.xyz`
- Chain ID: `177`
- Gas token: `HSK`
- Explorer: `https://hashkey.blockscout.com`

Mainnet proof for the DoraHacks HashKey Chain On-Chain Horizon submission:

- Contract address: `0x33145C082811c5E88ce055DAD816aE540a89da94`
- Contract explorer: `https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94`
- Anchor transaction: `https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6`
- Funding transaction: `https://hashkey.blockscout.com/tx/0x88262d336419b7592cf0582fb2aed823ce9c15033aab8a286c70f7195a2f96d4`

Deploy contract:

```bash
cp .env.example .env
# edit .env and add DEPLOYER_PRIVATE_KEY with a tiny HSK-funded deployer wallet
npm install
npm run compile
npm run test
npm run deploy:hashkey
```

After deployment, copy the address from `deployment/hashkey.json` into:

```bash
SCRATCH_REGISTRY_ADDRESS=0x...
```

Then run:

```bash
streamlit run app.py
```

Open **Anchor / Deploy** in the sidebar and check the RPC/contract status.

## Product demo flow

1. Choose bankroll: `100 USDC`.
2. Choose risk mode: `Normal`.
3. Click **Scratch Today**.
4. Show that most opportunities are rejected.
5. Show one small played opportunity.
6. Show one fake claim blocked by Claim Shield.
7. Generate report hash.
8. Click **Mock Anchor** or **Real HashKey Anchor**.
9. Show the Blockscout transaction if real anchoring is configured.

## Pitch

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet.

Users fund a tiny isolated wallet instead of connecting their main wallet. The agent scans HashKey Chain for small opportunities, including route edges, pool imbalances, incentive campaigns, and safe claims. Every action is simulated before execution, unsafe approvals are blocked, and the wallet stops automatically when predefined loss limits are reached.

Scratch Wallet treats small-wallet DeFi honestly: it can feel like scratching a lottery ticket, but the ticket should at least know when not to play.

## Safety boundaries

- The demo is dry-run first.
- The contract does not custody funds.
- The contract does not execute trades.
- Anchoring stores decision evidence only.
- Real execution should require a separate burner wallet and explicit opt-in.
- No yield or profit is promised.

## Repository map

```text
app.py                         Streamlit demo
engine/                        Python autonomous agent logic
contracts/ScratchWalletRegistry.sol
abi/ScratchWalletRegistry.abi.json
hardhat.config.cjs
scripts/deploy.js              HashKey deployment
docs/                          pitch, architecture, risk model, demo script
CODEX_NEXT_STEPS.md            minimal prompt for final polish
```


<!-- VIDEO_AUTOMATION_V4 -->
## Automated demo video

No manual screen recording required. This version includes Playwright + ffmpeg automation.

Windows PowerShell:

```powershell
scripts\record_demo.ps1
```

macOS / Linux / WSL:

```bash
./scripts/record_demo.sh
```

The output appears in `demo_recordings/scratch-wallet-demo-*/` with `scratch_wallet_demo.mp4`, `scratch_wallet_demo.webm`, screenshots, and subtitles. See `docs/video-recording.md`.

## v5 Wow Pack

This repository includes a near submission-ready Streamlit MVP:

- polished Streamlit UI with Demo, Scratch Card, Control Room, Claim Shield, Anchor/Deploy, Video/Submit pages;
- deterministic Python engines for scanning, simulation, risk modes, claim shielding, and autonomous scratch runs;
- Solidity registry contract for HashKey Chain decision anchoring;
- Playwright + ffmpeg demo recording scripts;
- one-command finalizer: `python scripts/one_click_final.py --skip-video`;
- copy-paste DoraHacks submission assets under `SUBMISSION_READY/`.

Core message: **A lottery ticket that knows when not to play.**


## BUIDL logo

The DoraHacks-ready 480×480 PNG logo is available at `assets/scratch-wallet-logo-480.png` and `SUBMISSION_READY/scratch-wallet-logo-480.png`.


## Final-mile files added in v7

- `SUBMISSION_READY/DORAHACKS_FORM_FIELDS.md` — exact copy/paste form fields.
- `SUBMISSION_READY/README_FOR_JUDGES.md` — short judge-facing README.
- `docs/final-operator-manual.md` — last-mile deployment/submission manual.
- `scripts/zero_effort_local_check.py` — preflight + tests + submission bundle.
- `scripts/github_publish_template.sh` / `.ps1` — push template for GitHub.

Fast check:

```bash
python scripts/zero_effort_local_check.py
streamlit run app.py
```
