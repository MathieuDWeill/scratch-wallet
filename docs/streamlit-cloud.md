# Streamlit Community Cloud deployment

## Minimum path

1. Create a GitHub repo named `scratch-wallet`.
2. Push this folder.
3. Go to Streamlit Community Cloud.
4. Click **New app**.
5. Repository: `scratch-wallet`.
6. Branch: `main`.
7. Main file path: `app.py`.
8. Click **Deploy**.

The app works without secrets using mock anchoring.

## Optional real HashKey anchor secrets

After deploying the contract, add these secrets in Streamlit Cloud → App → Settings → Secrets:

```toml
HASHKEY_RPC_URL = "https://mainnet.hsk.xyz"
HASHKEY_CHAIN_ID = "177"
SCRATCH_REGISTRY_ADDRESS = "0x..."
SCRATCH_WALLET_ADDRESS = "0x..."
ANCHOR_PRIVATE_KEY = "0x..."
```

Use a burner private key only. Never use a main wallet.

## Health check

Open the app → **Anchor / Deploy**. The RPC card should show Chain ID `177` and a latest block number.
