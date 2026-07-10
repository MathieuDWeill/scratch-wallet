# Deployment guide

## Streamlit Community Cloud

1. Create a public or private GitHub repository.
2. Push this project.
3. In Streamlit Community Cloud, create a new app.
4. Select `app.py` as the main file.
5. Add secrets only after you deploy the contract.

## HashKey Chain contract deployment

The repo includes Hardhat deployment plumbing.

HashKey mainnet configuration:

- RPC: `https://mainnet.hsk.xyz`
- Chain ID: `177`
- Explorer: `https://hashkey.blockscout.com`
- Gas token: `HSK`

Current mainnet deployment:

- Contract address: `0x33145C082811c5E88ce055DAD816aE540a89da94`
- Contract explorer: https://hashkey.blockscout.com/address/0x33145C082811c5E88ce055DAD816aE540a89da94
- Anchor transaction: https://hashkey.blockscout.com/tx/0x1bdbeac34080908bad17a491b76f212d455102195d2ff985cdd0384775329de6
- Funding transaction: https://hashkey.blockscout.com/tx/0x88262d336419b7592cf0582fb2aed823ce9c15033aab8a286c70f7195a2f96d4

```bash
cp .env.example .env
# edit .env
npm install
npm run compile
npm run test
npm run deploy:hashkey
```

Required `.env` values:

```env
HASHKEY_RPC_URL=https://mainnet.hsk.xyz
HASHKEY_CHAIN_ID=177
DEPLOYER_PRIVATE_KEY=0x...
```

After deployment:

```env
SCRATCH_REGISTRY_ADDRESS=0x...
SCRATCH_WALLET_ADDRESS=0x...
ANCHOR_PRIVATE_KEY=0x...
```

`ANCHOR_PRIVATE_KEY` should be a burner wallet with tiny HSK only.

## Real anchor flow

The Streamlit app calls `anchorDecision` on `ScratchWalletRegistry`.

It anchors:

- opportunity hash
- decision type hash
- risk mode hash
- bankroll size
- trade size
- gross/net edge bps
- risk score
- played/skipped boolean
- report hash

The contract does not execute trades and does not custody funds.
