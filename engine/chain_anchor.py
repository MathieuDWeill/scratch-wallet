from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
    from eth_account import Account
    from web3 import Web3
except Exception:  # Streamlit still boots if web3 deps fail
    load_dotenv = None
    Account = None
    Web3 = None

ABI_PATH = Path(__file__).resolve().parents[1] / "abi" / "ScratchWalletRegistry.abi.json"


@dataclass
class AnchorConfig:
    rpc_url: str
    chain_id: int
    contract_address: str | None
    private_key: str | None
    scratch_wallet_address: str | None


@dataclass
class AnchorResult:
    ok: bool
    mode: str
    message: str
    tx_hash: str | None = None
    explorer_url: str | None = None
    contract_address: str | None = None


def _secret(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st  # local import so engine remains CLI-safe
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return default


def load_anchor_config() -> AnchorConfig:
    if load_dotenv:
        load_dotenv()
    return AnchorConfig(
        rpc_url=_secret("HASHKEY_RPC_URL", "https://mainnet.hsk.xyz") or "https://mainnet.hsk.xyz",
        chain_id=int(_secret("HASHKEY_CHAIN_ID", "177") or "177"),
        contract_address=_secret("SCRATCH_REGISTRY_ADDRESS"),
        private_key=_secret("ANCHOR_PRIVATE_KEY") or _secret("DEPLOYER_PRIVATE_KEY"),
        scratch_wallet_address=_secret("SCRATCH_WALLET_ADDRESS"),
    )


def is_real_anchor_ready(config: AnchorConfig | None = None) -> tuple[bool, str]:
    config = config or load_anchor_config()
    if Web3 is None or Account is None:
        return False, "web3 dependencies unavailable"
    if not config.contract_address:
        return False, "SCRATCH_REGISTRY_ADDRESS missing"
    if not config.private_key:
        return False, "ANCHOR_PRIVATE_KEY missing"
    if not config.scratch_wallet_address:
        return False, "SCRATCH_WALLET_ADDRESS missing"
    return True, "ready"


def mock_anchor(report_hash: str, opportunity_hash: str | None = None) -> AnchorResult:
    fake = Web3.keccak(text=(report_hash + (opportunity_hash or ""))).hex() if Web3 else "0x" + report_hash[-32:]
    return AnchorResult(
        ok=True,
        mode="mock",
        message="Mock anchor generated. Configure secrets for a real HashKey Chain transaction.",
        tx_hash=fake,
        explorer_url=None,
    )


def _load_abi() -> list[dict[str, Any]]:
    return json.loads(ABI_PATH.read_text())


def _bytes32_hex(text: str) -> str:
    if text.startswith("0x") and len(text) == 66:
        return text
    if Web3 is None:
        raise RuntimeError("web3 unavailable")
    hashed = Web3.keccak(text=text).hex()
    return hashed if hashed.startswith("0x") else f"0x{hashed}"


def anchor_decision_real(
    *,
    opportunity_id: str,
    decision: str,
    risk_mode: str,
    starting_bankroll: float,
    trade_size: float,
    gross_edge_bps: int,
    net_edge_bps: int,
    risk_score: int,
    played: bool,
    report_hash: str,
    report_uri: str = "",
    config: AnchorConfig | None = None,
) -> AnchorResult:
    config = config or load_anchor_config()
    ready, reason = is_real_anchor_ready(config)
    if not ready:
        return AnchorResult(False, "real", reason)

    assert Web3 is not None and Account is not None
    w3 = Web3(Web3.HTTPProvider(config.rpc_url, request_kwargs={"timeout": 20}))
    if not w3.is_connected():
        return AnchorResult(False, "real", f"RPC not connected: {config.rpc_url}")
    remote_chain_id = int(w3.eth.chain_id)
    if remote_chain_id != int(config.chain_id):
        return AnchorResult(False, "real", f"Wrong chain id: RPC returned {remote_chain_id}, expected {config.chain_id}")

    account = Account.from_key(config.private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(config.contract_address), abi=_load_abi())
    scratch_wallet = Web3.to_checksum_address(config.scratch_wallet_address)
    report_hash32 = _bytes32_hex(report_hash)

    fn = contract.functions.anchorDecision(
        scratch_wallet,
        _bytes32_hex(opportunity_id),
        _bytes32_hex(decision),
        _bytes32_hex(risk_mode),
        int(round(starting_bankroll * 1_000_000)),
        int(round(trade_size * 1_000_000)),
        int(gross_edge_bps),
        int(net_edge_bps),
        int(max(0, min(100, risk_score))),
        bool(played),
        report_hash32,
        report_uri,
    )

    nonce = w3.eth.get_transaction_count(account.address)
    tx = fn.build_transaction({
        "from": account.address,
        "nonce": nonce,
        "chainId": int(config.chain_id),
        "gas": 350_000,
        "gasPrice": w3.eth.gas_price,
    })
    try:
        gas_estimate = w3.eth.estimate_gas(tx)
        tx["gas"] = int(gas_estimate * 1.25)
    except Exception:
        pass
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction if hasattr(signed, "rawTransaction") else signed.raw_transaction)
    tx_hex = tx_hash.hex()
    if not tx_hex.startswith("0x"):
        tx_hex = f"0x{tx_hex}"
    return AnchorResult(
        ok=True,
        mode="real",
        message="Anchored on HashKey Chain.",
        tx_hash=tx_hex,
        explorer_url=f"https://hashkey.blockscout.com/tx/{tx_hex}",
        contract_address=config.contract_address,
    )


def rpc_status(config: AnchorConfig | None = None) -> dict[str, Any]:
    config = config or load_anchor_config()
    if Web3 is None:
        return {"ok": False, "error": "web3 unavailable"}
    try:
        w3 = Web3(Web3.HTTPProvider(config.rpc_url, request_kwargs={"timeout": 10}))
        if not w3.is_connected():
            return {"ok": False, "error": "not connected", "rpc": config.rpc_url}
        return {
            "ok": True,
            "rpc": config.rpc_url,
            "chain_id": int(w3.eth.chain_id),
            "latest_block": int(w3.eth.block_number),
            "gas_price_wei": int(w3.eth.gas_price),
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc), "rpc": config.rpc_url}
