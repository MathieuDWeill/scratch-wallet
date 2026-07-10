# Final submission checklist

## Must-have
- [ ] App runs locally: `streamlit run app.py`
- [ ] `python scripts/preflight.py` passes
- [ ] GitHub repo pushed
- [ ] Streamlit Community Cloud app deployed
- [ ] Demo page works with “Scratch Today”
- [ ] Mock Anchor works
- [ ] Submission copy filled with GitHub + live demo URL
- [ ] 90-second demo video recorded

## Strongly recommended
- [ ] Hardhat compile passes
- [ ] Hardhat tests pass
- [ ] HashKey burner wallet funded with tiny HSK
- [ ] `ScratchWalletRegistry.sol` deployed to HashKey Chain
- [ ] `SCRATCH_REGISTRY_ADDRESS` added to Streamlit secrets
- [ ] Real HashKey Anchor button tested
- [ ] Example tx link added to DoraHacks submission

## Do not do
- [ ] Do not use your main wallet private key
- [ ] Do not promise guaranteed returns
- [ ] Do not claim the agent is live-trading real funds unless you actually implemented and tested that
- [ ] Do not add KYC/compliance scope
- [ ] Do not rebuild in JS


<!-- VIDEO_AUTOMATION_V4 -->
## Automated demo video

No manual screen recording required. This version includes Playwright + ffmpeg automation.

Windows PowerShell:

```powershell
scripts\record_demo.ps1
```

macOS / Linux / WSL:

```bash
./scripts/record_demo.sh
```

The output appears in `demo_recordings/scratch-wallet-demo-*/` with `scratch_wallet_demo.mp4`, `scratch_wallet_demo.webm`, screenshots, and subtitles. See `docs/video-recording.md`.
