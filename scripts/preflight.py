#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def check_file(path: str) -> None:
    p = ROOT / path
    if not p.exists():
        fail(f"Missing {path}")
    ok(f"Found {path}")


def main() -> None:
    print("Scratch Wallet preflight")
    print("========================")

    for path in [
        "app.py",
        "requirements.txt",
        "contracts/ScratchWalletRegistry.sol",
        "abi/ScratchWalletRegistry.abi.json",
        "SUBMISSION_READY/DORAHACKS_SUBMISSION.md",
        "SUBMISSION_READY/FINAL_CHECKLIST.md",
    ]:
        check_file(path)

    from engine.models import WalletState
    from engine.risk_modes import RISK_MODES
    from engine.scratch_engine import run_daily_scratch
    from engine.chain_anchor import load_anchor_config, rpc_status, is_real_anchor_ready

    wallet = WalletState(starting_bankroll=100.0, current_bankroll=100.0, risk_mode=RISK_MODES["Normal"])
    wallet, logs, simulations = run_daily_scratch(wallet)
    if not logs:
        fail("Scratch engine returned no logs")
    if wallet.trades_played + wallet.opportunities_skipped + wallet.rugs_dodged == 0:
        fail("Scratch engine did not update wallet state")
    ok(f"Scratch engine generated {len(logs)} decisions")

    abi = json.loads((ROOT / "abi/ScratchWalletRegistry.abi.json").read_text())
    names = {item.get("name") for item in abi if item.get("type") == "function"}
    needed = {"anchorDecision", "anchorSkippedOpportunity", "anchorWalletStopped", "anchorRugDodged", "getDecision"}
    missing = needed - names
    if missing:
        fail(f"ABI missing functions: {sorted(missing)}")
    ok("ABI exposes required registry functions")

    cfg = load_anchor_config()
    ready, reason = is_real_anchor_ready(cfg)
    if ready:
        ok("Real anchor secrets appear configured")
    else:
        warn(f"Real anchor not configured yet: {reason}")

    try:
        status = rpc_status(cfg)
        if status.get("ok"):
            ok(f"HashKey RPC connected: chain_id={status.get('chain_id')} block={status.get('latest_block')}")
        else:
            warn(f"HashKey RPC check failed: {status}")
    except Exception as exc:
        warn(f"RPC check skipped/failed: {exc}")

    if (ROOT / "node_modules").exists():
        try:
            subprocess.run(["npm", "run", "compile"], cwd=ROOT, check=True)
            ok("Hardhat compile passed")
        except Exception as exc:
            warn(f"Hardhat compile failed: {exc}")
    else:
        warn("node_modules not found; run `npm install` before Hardhat compile/test")

    print("\nPreflight complete. Next: streamlit run app.py")


if __name__ == "__main__":
    main()
