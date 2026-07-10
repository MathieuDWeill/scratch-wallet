#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

ROOT = Path(__file__).resolve().parents[1]
if load_dotenv:
    load_dotenv(ROOT / ".env")

keys = {
    "HASHKEY_RPC_URL": os.getenv("HASHKEY_RPC_URL", "https://mainnet.hsk.xyz"),
    "HASHKEY_CHAIN_ID": os.getenv("HASHKEY_CHAIN_ID", "177"),
    "SCRATCH_REGISTRY_ADDRESS": os.getenv("SCRATCH_REGISTRY_ADDRESS", "0x..."),
    "SCRATCH_WALLET_ADDRESS": os.getenv("SCRATCH_WALLET_ADDRESS", os.getenv("DEPLOYER_ADDRESS", "0x...")),
    "ANCHOR_PRIVATE_KEY": os.getenv("ANCHOR_PRIVATE_KEY", os.getenv("DEPLOYER_PRIVATE_KEY", "0x...")),
}

out = ROOT / ".streamlit" / "secrets.toml"
out.parent.mkdir(exist_ok=True)
text = "\n".join(f'{k} = "{v}"' for k, v in keys.items()) + "\n"
out.write_text(text)
print(f"Wrote {out}")
print("WARNING: .streamlit/secrets.toml is gitignored. Never commit private keys.")
