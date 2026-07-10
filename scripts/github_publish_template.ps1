param(
  [string]$RepoUrl = "https://github.com/mathieuweill/scratch-wallet.git"
)

if (-not (Test-Path .git)) { git init }
git add .
git commit -m "Submit Scratch Wallet"
git branch -M main
git remote remove origin 2>$null
git remote add origin $RepoUrl
git push -u origin main
