#!/usr/bin/env python3
from __future__ import annotations

try:
    from eth_account import Account
except Exception as exc:
    raise SystemExit(f"Install requirements first: pip install -r requirements.txt ({exc})")

acct = Account.create()
print("Generated fresh burner wallet")
print("==============================")
print(f"ADDRESS={acct.address}")
print(f"PRIVATE_KEY={acct.key.hex()}")
print()
print("WARNING: Use this only as a burner with tiny HSK. Never use or paste your main wallet private key.")
print("Add tiny HSK for deployment gas, then put PRIVATE_KEY into DEPLOYER_PRIVATE_KEY or ANCHOR_PRIVATE_KEY.")
