if (!(Test-Path .env)) {
  Copy-Item .env.example .env
  Write-Host "Created .env. Edit DEPLOYER_PRIVATE_KEY, then rerun this script."
  exit 1
}
npm install
npm run compile
npm run test
npm run deploy:hashkey
python scripts/write_streamlit_secrets_from_env.py
