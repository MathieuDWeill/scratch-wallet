from __future__ import annotations

import hashlib
import json
import textwrap
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine.chain_anchor import (
    anchor_decision_real,
    is_real_anchor_ready,
    load_anchor_config,
    mock_anchor,
    rpc_status,
)
from engine.claim_shield import inspect_claim
from engine.mock_data import OPPORTUNITIES
from engine.models import WalletState
from engine.narrator import daily_summary, roast_for_log
from engine.risk_modes import RISK_MODES
from engine.scratch_engine import run_daily_scratch
from engine.simulator import simulate

APP_NAME = "Scratch Wallet"
BUILDER = "Mathieu D. WEILL"
TAGLINE = "A lottery ticket that knows when not to play."
CHAIN = "HashKey Chain"

st.set_page_config(
    page_title="Scratch Wallet — Mathieu D. WEILL",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root { --gold: #f5c542; --cyan:#38bdf8; --pink:#fb7185; --green:#22c55e; --muted: #94a3b8; --bgcard: rgba(15,23,42,.74); }
.stApp { background: radial-gradient(circle at 20% 0%, rgba(245,197,66,.13), transparent 25%), radial-gradient(circle at 90% 10%, rgba(56,189,248,.13), transparent 28%), linear-gradient(180deg, #020617 0%, #0f172a 100%); }
.hero { padding: 1.55rem 1.75rem; border: 1px solid rgba(245,197,66,.38); border-radius: 26px; background: linear-gradient(135deg, rgba(245,197,66,.16), rgba(56,189,248,.08)); box-shadow: 0 18px 50px rgba(0,0,0,.28); }
.big {font-size: 4.2rem; line-height: .95; font-weight: 950; margin-bottom: .25rem; letter-spacing:-.055em;}
.tag {font-size: 1.38rem; color: var(--gold); font-weight: 800;}
.small-muted {color: var(--muted);} .tiny {font-size:.82rem;color:var(--muted)}
.card { padding: 1rem; border: 1px solid rgba(148,163,184,.24); border-radius: 18px; background: var(--bgcard); margin-bottom: .75rem; box-shadow: 0 10px 28px rgba(0,0,0,.18); }
.play {border-left: 6px solid #22c55e;} .skip {border-left: 6px solid #f97316;} .stop {border-left: 6px solid #ef4444;}
.badge {display:inline-block; padding:.18rem .55rem; border-radius:999px; background:rgba(245,197,66,.16); color:#fde68a; border:1px solid rgba(245,197,66,.28); font-size:.82rem; margin:.12rem .25rem .12rem 0;}
.badge2 {display:inline-block; padding:.18rem .55rem; border-radius:999px; background:rgba(56,189,248,.12); color:#bae6fd; border:1px solid rgba(56,189,248,.25); font-size:.82rem; margin:.12rem .25rem .12rem 0;}
.ok {color:#22c55e;font-weight:800}.warn{color:#f97316;font-weight:800}.bad{color:#ef4444;font-weight:800}.gold{color:#f5c542;font-weight:800}.cyan{color:#38bdf8;font-weight:800}
.block {border:1px solid rgba(148,163,184,.18); border-radius:16px; padding:1rem; background:rgba(2,6,23,.58); margin-bottom:.8rem;}
.scratch {border:1px dashed rgba(245,197,66,.55); background: linear-gradient(135deg, rgba(245,197,66,.10), rgba(15,23,42,.7)); border-radius:22px; padding:1.2rem;}
.kpi-label {font-size:.78rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em}.kpi-big{font-size:2.0rem;font-weight:900;letter-spacing:-.04em}.mono{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;}
hr {border-color: rgba(148,163,184,.16)!important;}
</style>
""",
    unsafe_allow_html=True,
)


def _json_hash(obj: dict) -> str:
    return "0x" + hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def make_report(wallet: WalletState, logs: list) -> dict:
    rows = [asdict(log) for log in logs]
    return {
        "project": APP_NAME,
        "builder": BUILDER,
        "chain": CHAIN,
        "tagline": TAGLINE,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "bankroll": wallet.starting_bankroll,
        "risk_mode": wallet.risk_mode.name,
        "current_bankroll": wallet.current_bankroll,
        "realized_pnl": wallet.realized_pnl,
        "realized_pnl_pct": round(wallet.realized_pnl / max(wallet.starting_bankroll, 1) * 100, 4),
        "trades_played": wallet.trades_played,
        "opportunities_skipped": wallet.opportunities_skipped,
        "rugs_dodged": wallet.rugs_dodged,
        "logs": rows,
        "thesis": "Autonomous finance should start with bounded downside.",
    }


def report_hash(report: dict) -> str:
    return _json_hash(report)


def style_decision(log) -> str:
    return "play" if log.decision == "PLAY" else "stop" if log.decision == "STOP" else "skip"


def run_demo(bankroll: float, mode_name: str) -> None:
    wallet = WalletState(starting_bankroll=bankroll, current_bankroll=bankroll, risk_mode=RISK_MODES[mode_name])
    wallet, logs, simulations = run_daily_scratch(wallet)
    st.session_state["wallet"] = wallet
    st.session_state["logs"] = logs
    st.session_state["simulations"] = simulations
    st.session_state.pop("anchor_result", None)


def ensure_demo(bankroll: float, mode_name: str) -> tuple[WalletState, list, list]:
    if "logs" not in st.session_state:
        run_demo(bankroll, mode_name)
    return st.session_state["wallet"], st.session_state["logs"], st.session_state["simulations"]


def share_card_svg(report: dict) -> str:
    pnl = report["realized_pnl"]
    pnl_color = "#22c55e" if pnl >= 0 else "#ef4444"
    return f"""<svg width=\"1200\" height=\"630\" xmlns=\"http://www.w3.org/2000/svg\">
<defs><linearGradient id=\"g\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"1\"><stop stop-color=\"#020617\"/><stop offset=\"1\" stop-color=\"#172554\"/></linearGradient></defs>
<rect width=\"1200\" height=\"630\" fill=\"url(#g)\"/>
<circle cx=\"1020\" cy=\"70\" r=\"230\" fill=\"#38bdf8\" opacity=\"0.14\"/>
<circle cx=\"180\" cy=\"20\" r=\"230\" fill=\"#f5c542\" opacity=\"0.16\"/>
<rect x=\"64\" y=\"64\" width=\"1072\" height=\"502\" rx=\"34\" fill=\"#0f172a\" opacity=\"0.82\" stroke=\"#f5c542\" stroke-opacity=\"0.45\"/>
<text x=\"96\" y=\"145\" fill=\"#f8fafc\" font-family=\"Arial, sans-serif\" font-size=\"76\" font-weight=\"900\">Scratch Wallet</text>
<text x=\"100\" y=\"196\" fill=\"#f5c542\" font-family=\"Arial, sans-serif\" font-size=\"32\" font-weight=\"700\">A lottery ticket that knows when not to play.</text>
<text x=\"100\" y=\"274\" fill=\"#94a3b8\" font-family=\"Arial, sans-serif\" font-size=\"28\">Risk mode</text>
<text x=\"100\" y=\"326\" fill=\"#e2e8f0\" font-family=\"Arial, sans-serif\" font-size=\"46\" font-weight=\"800\">{report['risk_mode']}</text>
<text x=\"420\" y=\"274\" fill=\"#94a3b8\" font-family=\"Arial, sans-serif\" font-size=\"28\">P&amp;L</text>
<text x=\"420\" y=\"326\" fill=\"{pnl_color}\" font-family=\"Arial, sans-serif\" font-size=\"46\" font-weight=\"800\">{pnl:+.4f} USDC</text>
<text x=\"760\" y=\"274\" fill=\"#94a3b8\" font-family=\"Arial, sans-serif\" font-size=\"28\">Rugs dodged</text>
<text x=\"760\" y=\"326\" fill=\"#38bdf8\" font-family=\"Arial, sans-serif\" font-size=\"46\" font-weight=\"800\">{report['rugs_dodged']}</text>
<text x=\"100\" y=\"430\" fill=\"#cbd5e1\" font-family=\"Arial, sans-serif\" font-size=\"28\">Played {report['trades_played']} · Skipped {report['opportunities_skipped']} · Report anchored on HashKey-ready audit trail</text>
<text x=\"100\" y=\"500\" fill=\"#f8fafc\" font-family=\"Arial, sans-serif\" font-size=\"26\" font-weight=\"700\">Built by Mathieu D. WEILL</text>
</svg>"""


def submission_markdown(report: dict | None = None) -> str:
    extra = ""
    if report:
        extra = f"""

Latest demo run:
- Starting bankroll: {report['bankroll']:.2f} USDC
- Current bankroll: {report['current_bankroll']:.4f} USDC
- P&L: {report['realized_pnl']:+.4f} USDC
- Played opportunities: {report['trades_played']}
- Skipped opportunities: {report['opportunities_skipped']}
- Rugs dodged: {report['rugs_dodged']}
- Report hash: {report_hash(report)}
"""
    return f"""# Scratch Wallet

**Builder:** Mathieu D. WEILL  
**Track:** AI / DeFi  
**Chain:** HashKey Chain  
**Tagline:** A lottery ticket that knows when not to play.

Scratch Wallet is a risk-capped autonomous DeFi micro-wallet. Users fund a tiny isolated wallet instead of connecting their main wallet. The agent scans HashKey Chain for small opportunities such as route edges, pool imbalances, incentives, and safe claims. Every action is simulated before execution, dangerous approvals are blocked, and the wallet stops automatically when predefined loss limits are reached.

The project treats small-wallet DeFi honestly: it can feel like scratching a lottery ticket, but the ticket should at least know when not to play.

## Why it matters

Autonomous trading agents are dangerous when they get access to valuable wallets, overtrade, ignore slippage, or sign unsafe approvals. Scratch Wallet flips the model: bounded bankroll first, autonomy second.

## What the demo shows

1. Create a tiny isolated wallet.
2. Choose Chicken, Normal, or Degen mode.
3. Run the autonomous scratch.
4. Watch the agent reject most opportunities.
5. See Claim Shield block a fake airdrop.
6. Generate a deterministic audit report.
7. Anchor the decision report on HashKey Chain, or use the mock anchor in local mode.

## Core thesis

Autonomous finance should start with bounded downside.{extra}
"""


with st.sidebar:
    st.title("🎫 Scratch Wallet")
    st.caption("by Mathieu D. WEILL")
    pages = [
        "Demo",
        "Scratch Card",
        "Control Room",
        "Claim Shield",
        "Anchor / Deploy",
        "Opportunities",
        "Video / Submit",
        "Risk Model",
        "Submission",
        "Form Fields",
        "Codex",
    ]
    requested_page = st.query_params.get("page", "Demo")
    page_index = pages.index(requested_page) if requested_page in pages else 0
    page = st.radio("Navigation", pages, index=page_index)
    st.divider()
    bankroll = st.number_input("Tiny wallet bankroll (USDC)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
    mode_name = st.selectbox("Risk mode", list(RISK_MODES.keys()), index=1)
    st.caption("No main wallet. No unlimited downside.")
    if st.button("⚡ Preload demo run", use_container_width=True):
        run_demo(bankroll, mode_name)

mode = RISK_MODES[mode_name]

if page == "Demo":
    st.markdown(
        f"""
    <div class="hero">
      <div class="big">Scratch Wallet</div>
      <div class="tag">{TAGLINE}</div>
      <p class="small-muted">A risk-capped autonomous DeFi micro-wallet for HashKey Chain. Fund a tiny isolated wallet, choose a risk mode, and let the agent hunt for small opportunities while refusing unsafe trades, approvals, and claims.</p>
      <span class="badge">bounded downside</span><span class="badge">autonomous micro-wallet</span><span class="badge">claim shield</span><span class="badge">HashKey audit trail</span><span class="badge2">built by Mathieu D. WEILL</span>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bankroll", f"{bankroll:.2f} USDC")
    col2.metric("Mode", mode.name)
    col3.metric("Max trade", f"{bankroll * mode.max_trade_pct:.2f} USDC")
    col4.metric("Max daily loss", f"{bankroll * mode.max_daily_loss_pct:.2f} USDC")

    c1, c2, c3 = st.columns([2, 1, 1])
    if c1.button("🎫 Scratch Today", type="primary", use_container_width=True):
        run_demo(bankroll, mode_name)
    if c2.button("Reset", use_container_width=True):
        for key in ["wallet", "logs", "simulations", "anchor_result"]:
            st.session_state.pop(key, None)
    if c3.button("Record-ready demo", use_container_width=True):
        run_demo(100.0, "Normal")

    if "logs" not in st.session_state:
        st.info("Click **Scratch Today** to run the autonomous daily demo.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""<div class='block'><b>1. Tiny wallet</b><br><span class='small-muted'>No main wallet. Only bounded bankroll.</span></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class='block'><b>2. Paranoid agent</b><br><span class='small-muted'>Rejects most opportunities by design.</span></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='block'><b>3. HashKey audit</b><br><span class='small-muted'>Every decision can be anchored.</span></div>""", unsafe_allow_html=True)
    else:
        wallet = st.session_state["wallet"]
        logs = st.session_state["logs"]
        report = make_report(wallet, logs)
        rhash = report_hash(report)
        st.success(daily_summary(wallet, logs))

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Current bankroll", f"{wallet.current_bankroll:.4f}")
        c2.metric("Realized P&L", f"{wallet.realized_pnl:+.4f}", f"{wallet.realized_pnl / wallet.starting_bankroll * 100:+.2f}%")
        c3.metric("Played", wallet.trades_played)
        c4.metric("Skipped", wallet.opportunities_skipped)
        c5.metric("Rugs dodged", wallet.rugs_dodged)
        c6.metric("Report hash", rhash[:10] + "…")

        pnl_fig = go.Figure()
        values = [wallet.starting_bankroll]
        running = wallet.starting_bankroll
        labels = ["Start"]
        for idx, log in enumerate(logs, start=1):
            running += log.pnl_usd
            values.append(running)
            labels.append(f"{idx}. {log.decision}")
        pnl_fig.add_trace(go.Scatter(x=labels, y=values, mode="lines+markers", name="Bankroll"))
        pnl_fig.update_layout(title="Bankroll path — tiny wallet only", height=300, margin=dict(l=15, r=15, t=45, b=15))
        st.plotly_chart(pnl_fig, use_container_width=True)

        st.subheader("Scratch Journal")
        for log in logs:
            st.markdown(
                f"""
            <div class="card {style_decision(log)}">
              <b>{log.decision}</b> — {log.title}<br>
              <span class="small-muted">Net edge: {log.net_edge_bps} bps · Risk: {log.risk_score}/100 · Size: {log.trade_size_usd:.2f} USDC · P&L: {log.pnl_usd:+.4f}</span><br>
              {log.reason}<br>
              <i>{roast_for_log(log)}</i><br>
              <span class="tiny">Local decision hash: {log.tx_hash}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        rows = [asdict(log) for log in logs]
        df = pd.DataFrame(rows)
        left, right = st.columns([1, 1])
        with left:
            counts = df["decision"].value_counts().reset_index()
            counts.columns = ["decision", "count"]
            st.plotly_chart(px.pie(counts, names="decision", values="count", hole=.48, title="Decision mix"), use_container_width=True)
        with right:
            st.plotly_chart(px.bar(df, x="opportunity_id", y="net_edge_bps", color="decision", title="Net edge by candidate"), use_container_width=True)

        st.subheader("HashKey Chain anchor")
        st.code(rhash)
        ready, reason = is_real_anchor_ready(load_anchor_config())
        if ready:
            st.markdown("<span class='ok'>Real anchor configured.</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='warn'>Real anchor not configured:</span> {reason}. Mock anchor remains available for local demo.", unsafe_allow_html=True)

        a1, a2, a3, a4 = st.columns([1, 1, 1.2, 1.2])
        if a1.button("Mock Anchor", use_container_width=True):
            first = logs[0] if logs else None
            res = mock_anchor(rhash, first.opportunity_id if first else "daily")
            st.session_state["anchor_result"] = asdict(res)
        if a2.button("Real HashKey Anchor", use_container_width=True, disabled=not ready):
            first_play = next((x for x in logs if x.decision == "PLAY"), logs[0])
            res = anchor_decision_real(
                opportunity_id=first_play.opportunity_id,
                decision=first_play.decision,
                risk_mode=wallet.risk_mode.name,
                starting_bankroll=wallet.starting_bankroll,
                trade_size=first_play.trade_size_usd,
                gross_edge_bps=first_play.net_edge_bps + 15,
                net_edge_bps=first_play.net_edge_bps,
                risk_score=first_play.risk_score,
                played=first_play.decision == "PLAY",
                report_hash=rhash,
                report_uri="",
            )
            st.session_state["anchor_result"] = asdict(res)
        a3.download_button("Download report JSON", json.dumps(report, indent=2), file_name="scratch_wallet_report.json", use_container_width=True)
        a4.download_button("Download share card SVG", share_card_svg(report), file_name="scratch_wallet_share_card.svg", mime="image/svg+xml", use_container_width=True)

        if "anchor_result" in st.session_state:
            result = st.session_state["anchor_result"]
            if result.get("ok"):
                st.success(result.get("message"))
                st.code(result.get("tx_hash"))
                if result.get("explorer_url"):
                    st.link_button("Open tx on HashKey Blockscout", result["explorer_url"])
            else:
                st.error(result.get("message"))

elif page == "Scratch Card":
    wallet, logs, simulations = ensure_demo(bankroll, mode_name)
    report = make_report(wallet, logs)
    st.title("🎫 Daily Scratch Card")
    st.caption("This is the shareable artifact: simple, memorable, and judge-friendly.")
    st.markdown(
        f"""
        <div class="scratch">
          <div class="kpi-label">Today's scratch result</div>
          <div class="kpi-big">{wallet.realized_pnl:+.4f} USDC</div>
          <p><span class="badge">{wallet.risk_mode.name} mode</span><span class="badge">{wallet.trades_played} played</span><span class="badge">{wallet.opportunities_skipped} skipped</span><span class="badge">{wallet.rugs_dodged} rug dodged</span></p>
          <p class="small-muted">Bot mood: <b>Still poor, but alive.</b></p>
          <p class="small-muted mono">Report hash: {report_hash(report)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Best hit")
        plays = [x for x in logs if x.decision == "PLAY"]
        if plays:
            best = max(plays, key=lambda x: x.pnl_usd)
            st.success(f"{best.title}: {best.pnl_usd:+.4f} USDC")
            st.write(best.reason)
        else:
            st.warning("No trade played. That is acceptable: rejected opportunities are a feature.")
    with c2:
        st.subheader("Best dodge")
        dodges = [x for x in logs if "Rug dodged" in x.reason]
        if dodges:
            st.error(dodges[0].title)
            st.write(dodges[0].reason)
        else:
            st.info("No rug was detected in this run.")
    st.download_button("Download share card SVG", share_card_svg(report), file_name="scratch_wallet_share_card.svg", mime="image/svg+xml")

elif page == "Control Room":
    wallet, logs, simulations = ensure_demo(bankroll, mode_name)
    st.title("Autopilot Control Room")
    st.caption("A serious quant-style view of a deliberately tiny and paranoid autonomous wallet.")
    sim_rows = []
    for sim in simulations:
        sim_rows.append({
            "id": sim.opportunity.id,
            "title": sim.opportunity.title,
            "kind": sim.opportunity.kind,
            "gross_bps": sim.opportunity.gross_edge_bps,
            "net_bps": sim.net_edge_bps,
            "risk": sim.opportunity.risk_score,
            "slippage_bps": sim.opportunity.estimated_slippage_bps,
            "liquidity_usd": sim.opportunity.liquidity_usd,
            "recommendation": sim.recommendation,
            "reason": "; ".join(sim.reasons),
        })
    df = pd.DataFrame(sim_rows)
    top = st.columns(5)
    top[0].metric("Scanned", len(df))
    top[1].metric("Rejected", int((df["recommendation"] != "PLAY").sum()))
    top[2].metric("Played", int((df["recommendation"] == "PLAY").sum()))
    top[3].metric("Avg risk", f"{df['risk'].mean():.1f}/100")
    top[4].metric("Survival", "ON")
    st.plotly_chart(px.scatter(df, x="risk", y="net_bps", color="recommendation", size="liquidity_usd", hover_name="title", title="Autopilot decision surface"), use_container_width=True)
    st.dataframe(df, use_container_width=True)

elif page == "Claim Shield":
    st.title("Claim Shield")
    st.caption("The scam-protection layer inside Scratch Wallet. It blocks unsafe claims before the tiny wallet signs anything.")
    claim_ops = [o for o in OPPORTUNITIES if "claim" in o.kind]
    selected = st.selectbox("Pick a claim scenario", [o.title for o in claim_ops])
    op = next(o for o in claim_ops if o.title == selected)
    result = inspect_claim(op)
    c1, c2, c3 = st.columns(3)
    c1.metric("Claim risk", result["risk"])
    c2.metric("Safe", "YES" if result["safe"] else "NO")
    c3.metric("Approval request", op.approval_request or "none")
    if result["safe"]:
        st.success(result["finding"])
    else:
        st.error(result["finding"])
    st.markdown("### Plain-English verdict")
    if result["safe"]:
        st.write("This claim does not ask for permissions unrelated to receiving the reward. It may still be tiny-wallet only, but the mock scanner does not detect a drainer pattern.")
    else:
        st.write("This is not a normal claim. It asks for a permission that can expose assets. Scratch Wallet skips it and records the event as a rug dodged.")
        st.markdown("> This is not an airdrop. This is a wallet drainer wearing a party hat.")
    st.json(result)

elif page == "Anchor / Deploy":
    st.title("Anchor / Deploy")
    st.caption("Everything needed to avoid burning Codex credits on deployment plumbing.")
    cfg = load_anchor_config()
    status = rpc_status(cfg)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("RPC", "OK" if status.get("ok") else "ERR")
    col2.metric("Chain ID", status.get("chain_id", "—"))
    col3.metric("Latest block", status.get("latest_block", "—"))
    col4.metric("Gas wei", status.get("gas_price_wei", "—"))
    if not status.get("ok"):
        st.warning(status)

    ready, reason = is_real_anchor_ready(cfg)
    st.subheader("Runtime config")
    st.write({
        "HASHKEY_RPC_URL": cfg.rpc_url,
        "HASHKEY_CHAIN_ID": cfg.chain_id,
        "SCRATCH_REGISTRY_ADDRESS": cfg.contract_address or "missing",
        "SCRATCH_WALLET_ADDRESS": cfg.scratch_wallet_address or "missing",
        "ANCHOR_PRIVATE_KEY": "set" if cfg.private_key else "missing",
        "real_anchor_ready": ready,
        "reason": reason,
    })

    st.subheader("Deploy commands")
    st.code(
        """cp .env.example .env
# edit .env and add DEPLOYER_PRIVATE_KEY with a tiny HSK-funded deployer wallet
npm install
npm run compile
npm run test
npm run deploy:hashkey
# copy the deployed address from deployment/hashkey.json into SCRATCH_REGISTRY_ADDRESS
streamlit run app.py""",
        language="bash",
    )
    st.subheader("Streamlit Community Cloud secrets")
    st.code(
        '''HASHKEY_RPC_URL = "https://mainnet.hsk.xyz"
HASHKEY_CHAIN_ID = "177"
SCRATCH_REGISTRY_ADDRESS = "0x..."
SCRATCH_WALLET_ADDRESS = "0x..."
ANCHOR_PRIVATE_KEY = "0x..."''',
        language="toml",
    )
    st.error("Use a fresh burner wallet with tiny HSK only. Never paste your main wallet private key in Streamlit secrets.")

elif page == "Opportunities":
    st.title("Opportunity Scanner")
    st.caption("Mock opportunities used by the autonomous demo. Codex does not need to invent the scoring logic; it is already implemented in Python.")
    df = pd.DataFrame([asdict(o) | {"route": " → ".join(o.route)} for o in OPPORTUNITIES])
    st.dataframe(df[["id", "title", "kind", "route", "protocol", "gross_edge_bps", "estimated_slippage_bps", "liquidity_usd", "risk_score", "confidence", "approval_request", "verified_contract"]], use_container_width=True)
    st.plotly_chart(px.scatter(df, x="risk_score", y="gross_edge_bps", size="liquidity_usd", color="kind", hover_name="title", title="Edge vs Risk"), use_container_width=True)

elif page == "Video / Submit":
    st.title("Video / Submit Pack")
    st.caption("The repo includes an automated Playwright + ffmpeg video pipeline and copy-paste submission files.")
    st.markdown("""
### One-shot video commands

Windows PowerShell:
```powershell
scripts\\record_demo.ps1
```

Linux / WSL / macOS:
```bash
./scripts/record_demo.sh
```

Output:
```text
demo_recordings/<timestamp>/scratch_wallet_demo.mp4
```
""")
    wallet, logs, simulations = ensure_demo(100.0, "Normal")
    report = make_report(wallet, logs)
    st.download_button("Download DoraHacks submission markdown", submission_markdown(report), file_name="DORAHACKS_SUBMISSION_FINAL.md", use_container_width=True)
    st.download_button("Download share card SVG", share_card_svg(report), file_name="scratch_wallet_share_card.svg", mime="image/svg+xml", use_container_width=True)
    st.code("python scripts/one_click_final.py --skip-video", language="bash")

elif page == "Risk Model":
    st.title("Risk Model")
    st.markdown(
        """
Scratch Wallet is deliberately paranoid. It rejects most opportunities by design.

**Hard rules**
- isolated tiny wallet only;
- max trade size per mode;
- max daily loss;
- max total drawdown;
- allowed tokens only;
- slippage cap;
- liquidity floor;
- unsafe approvals blocked;
- suspicious claims skipped;
- no unverified contracts.

**Core principle**
> Autonomous finance should start with bounded downside.
"""
    )
    mode_df = pd.DataFrame([asdict(m) | {"allowed_tokens": ", ".join(m.allowed_tokens), "allowed_types": ", ".join(m.allowed_types)} for m in RISK_MODES.values()])
    st.dataframe(mode_df, use_container_width=True)

elif page == "Submission":
    st.title("Submission Copy")
    report = None
    if "logs" in st.session_state:
        report = make_report(st.session_state["wallet"], st.session_state["logs"])
    st.markdown(submission_markdown(report))
    st.download_button("Download final submission markdown", submission_markdown(report), file_name="DORAHACKS_SUBMISSION_FINAL.md", use_container_width=True)


elif page == "Form Fields":
    st.title("DoraHacks Form Fields")
    st.caption("Copy/paste fields for the BUIDL creation form. Replace URLs after GitHub, Streamlit, and YouTube are live.")
    vision = """Autonomous DeFi agents are exciting, but most of them start from a dangerous assumption: users connect a valuable main wallet and trust an automated system to trade, claim, approve, or interact with contracts.

Scratch Wallet solves this by making autonomous DeFi start with bounded downside.

Users fund a tiny isolated wallet instead of connecting their main wallet. The agent scans HashKey Chain for small opportunities such as route edges, pool imbalances, incentive campaigns, and safe claims. Every action is simulated before execution, dangerous approvals are blocked through Claim Shield, most opportunities are rejected, and the wallet stops automatically when predefined risk limits are reached.

The product treats small-wallet DeFi honestly: it can feel like scratching a lottery ticket, but the ticket should at least know when not to play.

Scratch Wallet combines autonomous execution, bankroll limits, Claim Shield protection, and on-chain decision anchoring to create a safer model for consumer-facing DeFi agents."""
    st.text_input("BUIDL name", "Scratch Wallet")
    st.text_area("Vision", vision, height=290)
    st.text_input("Category", "DeFi, AI, Security")
    st.text_input("Is this BUIDL an AI Agent?", "Yes")
    st.text_input("GitHub", "https://github.com/mathieuweill/scratch-wallet")
    st.text_input("Project website", "https://scratch-wallet.streamlit.app")
    st.text_input("Demo video", "https://www.youtube.com/watch?v=REPLACE_ME")
    st.text_area("Social links", "https://www.linkedin.com/in/mathieuweill\nhttps://x.com/mathieuweill\nhttps://mathieuweill.com", height=100)
    st.info("Logo file inside the repo: SUBMISSION_READY/scratch-wallet-logo-480.png")
    st.download_button("Download form fields markdown", Path("SUBMISSION_READY/DORAHACKS_FORM_FIELDS.md").read_text(encoding="utf-8"), file_name="DORAHACKS_FORM_FIELDS.md", use_container_width=True)

elif page == "Codex":
    st.title("Codex Next Steps")
    st.markdown(
        """
Most plumbing is already included now. Codex should only polish, not build from scratch.

1. Run the Streamlit app and fix any UI regressions.
2. Deploy `ScratchWalletRegistry.sol` if you have a tiny funded HashKey deployer wallet.
3. Paste the contract address into `.env` or Streamlit secrets.
4. Test `Real HashKey Anchor` from the demo page.
5. Record the 90-second video.

Recommended Codex prompt:

```text
This is Scratch Wallet by Mathieu D. WEILL. Most of the implementation is already done. Do not rewrite the project. Run it, fix bugs, polish the Streamlit UI, deploy ScratchWalletRegistry to HashKey Chain if credentials are available, wire/check the real anchor flow, and prepare the hackathon submission.
```
"""
    )
