# Final Operator Manual

This file is for the last mile. Follow it top to bottom.

## 1. Run locally

```bash
pip install -r requirements.txt
python scripts/preflight.py
streamlit run app.py
```

## 2. Push to GitHub

```bash
git init
git add .
git commit -m "Submit Scratch Wallet"
git branch -M main
git remote add origin https://github.com/MathieuDWeill/scratch-wallet.git
git push -u origin main
```

## 3. Deploy Streamlit Community Cloud

- New app
- Repo: `MathieuDWeill/scratch-wallet`
- Branch: `main`
- Main file: `app.py`

## 4. Generate video

```bash
pip install -r requirements-video.txt
python -m playwright install chromium
python scripts/one_click_final.py
```

Upload the MP4 to YouTube as unlisted.

## 5. Optional HashKey contract deploy

Use a burner wallet with tiny HSK only. Never use a main wallet.

```bash
npm install
npm run compile
npm run test
npm run deploy:hashkey
```

Copy the deployed address into Streamlit secrets.

## 6. Submit on DoraHacks

Open:

```text
SUBMISSION_READY/DORAHACKS_FORM_FIELDS.md
```

Copy the fields into the form.
