# Minimal Codex prompt

```text
This repo is Scratch Wallet by Mathieu D. WEILL for the HashKey Chain On-Chain Horizon Hackathon.

Do not rewrite the project.
Do not convert it to React.
Do not invent a new product.

Goal: make the existing Streamlit MVP submission-ready with minimum changes.

Steps:
1. Run `python scripts/preflight.py`.
2. Run `streamlit run app.py` and fix only runtime errors.
3. Run `npm install && npm run compile && npm run test` if Node is available.
4. If a tiny funded HashKey burner wallet is available, deploy `ScratchWalletRegistry.sol` with `npm run deploy:hashkey`.
5. Put the deployed contract address into Streamlit secrets.
6. Test the Real HashKey Anchor button.
7. Update `SUBMISSION_READY/DORAHACKS_SUBMISSION.md` with the live app URL, GitHub URL, contract address, and demo video URL.
8. Keep the core positioning unchanged: Scratch Wallet is a risk-capped autonomous DeFi micro-wallet. Tagline: “A lottery ticket that knows when not to play.”
```
