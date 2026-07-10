# RUN ME FIRST — Scratch Wallet

Scratch Wallet is a Streamlit MVP by **Mathieu D. WEILL**.

Core line: **A lottery ticket that knows when not to play.**

## Fastest local run

```bash
pip install -r requirements.txt
python scripts/preflight.py
streamlit run app.py
```

Then click:

1. `Scratch Today`
2. `Scratch Card`
3. `Claim Shield`
4. `Anchor / Deploy`
5. `Video / Submit`

## One-command finalizer

Without video:

```bash
python scripts/one_click_final.py --skip-video
```

With automated Playwright/ffmpeg video:

```bash
python scripts/one_click_final.py
```

## Windows video only

```powershell
scripts\record_demo.ps1
```

## Linux / WSL / macOS video only

```bash
./scripts/record_demo.sh
```

## Deploy HashKey registry

Use a **fresh burner wallet with tiny HSK only**.

```bash
cp .env.example .env
# edit DEPLOYER_PRIVATE_KEY
npm install
npm run compile
npm run test
npm run deploy:hashkey
```

Then copy the contract address from `deployment/hashkey.json` into Streamlit secrets or `.env`.

## Submit

Copy from:

```text
SUBMISSION_READY/DORAHACKS_SUBMISSION.md
SUBMISSION_READY/JUDGE_QA.md
SUBMISSION_READY/VIDEO_SCRIPT_90_SECONDS.md
```

The repo is designed so Codex should only fix local environment bugs or deploy with credentials, not rebuild the product.


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
