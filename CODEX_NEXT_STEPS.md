# Codex next steps — do not rebuild

The project is already implemented as a Streamlit MVP with Python engines, Solidity contract, Hardhat deploy, and real/mock HashKey anchoring.

## Goal

Finalize Scratch Wallet for hackathon submission without spending many cycles.

## Priority order

1. **Run locally**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
   Fix only actual runtime errors.

2. **Check Python syntax**
   ```bash
   python -m compileall app.py engine scripts
   ```

3. **Deploy contract if a tiny HSK-funded burner wallet is available**
   ```bash
   cp .env.example .env
   # add DEPLOYER_PRIVATE_KEY
   npm install
   npm run compile
   npm run test
   npm run deploy:hashkey
   ```

4. **Wire real anchor**
   Set:
   ```bash
   SCRATCH_REGISTRY_ADDRESS=0x...
   SCRATCH_WALLET_ADDRESS=0x...
   ANCHOR_PRIVATE_KEY=0x...
   ```
   Then test **Real HashKey Anchor** in the app.

5. **Streamlit Cloud**
   - push repo to GitHub
   - create app with main file `app.py`
   - paste secrets from `.streamlit/secrets.toml.example`

6. **Submission**
   Use `docs/submission.md` and record `docs/demo-script.md` as a 90-second video.

## Do not change

- Project name: Scratch Wallet
- Builder: Mathieu D. WEILL
- Core tagline: A lottery ticket that knows when not to play.
- Product principle: autonomous finance should start with bounded downside.
- Safety design: isolated tiny wallet, hard limits, Claim Shield, dry-run first.

## Nice polish only if time remains

- improve visual design
- add a deployed contract badge to the landing page
- add real Blockscout links after anchoring
- add one live RPC read such as latest block, gas price, or wallet HSK balance
- generate screenshot assets for DoraHacks
