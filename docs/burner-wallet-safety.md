# Burner wallet safety

Scratch Wallet is designed around isolated downside.

Use a fresh burner wallet for:

- contract deployment;
- report anchoring;
- future tiny-wallet execution experiments.

Never use:

- your main wallet;
- a wallet with NFTs;
- a wallet with significant ETH/HSK/stablecoin balances;
- a reused wallet with existing approvals.

Recommended workflow:

1. Generate a burner wallet with `python scripts/generate_burner_wallet.py`.
2. Fund it with the smallest amount of HSK needed for deployment/anchoring gas.
3. Deploy the registry.
4. Use that same burner only for demo anchoring.
5. Rotate the key after the hackathon if needed.

Scratch Wallet is a hackathon MVP, not a custody product and not financial advice.
