const fs = require("fs");
const path = require("path");

function writeDeploymentHelpers(out, deployerAddress) {
  const root = path.join(__dirname, "..");
  fs.mkdirSync(path.join(root, "deployment"), { recursive: true });
  fs.writeFileSync(path.join(root, "deployment", "hashkey.json"), JSON.stringify(out, null, 2));

  const envDeployed = [
    `HASHKEY_RPC_URL=${out.rpc}`,
    `HASHKEY_CHAIN_ID=${out.chainId}`,
    `SCRATCH_REGISTRY_ADDRESS=${out.address}`,
    `SCRATCH_WALLET_ADDRESS=${deployerAddress}`,
    `# ANCHOR_PRIVATE_KEY=put_the_same_burner_private_key_here_for_streamlit_anchor_only`,
    ""
  ].join("\n");
  fs.writeFileSync(path.join(root, "deployment", ".env.deployed.example"), envDeployed);

  const streamlitSecrets = [
    `HASHKEY_RPC_URL = "${out.rpc}"`,
    `HASHKEY_CHAIN_ID = "${out.chainId}"`,
    `SCRATCH_REGISTRY_ADDRESS = "${out.address}"`,
    `SCRATCH_WALLET_ADDRESS = "${deployerAddress}"`,
    `ANCHOR_PRIVATE_KEY = "0x..."`,
    ""
  ].join("\n");
  fs.writeFileSync(path.join(root, "deployment", "streamlit_secrets.toml"), streamlitSecrets);
}

async function main() {
  const [deployer] = await ethers.getSigners();
  const network = await ethers.provider.getNetwork();
  console.log("Deploying ScratchWalletRegistry");
  console.log("Network:", network.name, Number(network.chainId));
  console.log("Deployer:", deployer.address);
  console.log("Balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "HSK/ETH units");

  const Factory = await ethers.getContractFactory("ScratchWalletRegistry");
  const registry = await Factory.deploy();
  await registry.waitForDeployment();
  const address = await registry.getAddress();
  const tx = registry.deploymentTransaction();

  console.log("Contract:", address);
  console.log("Deploy tx:", tx.hash);
  console.log("Explorer:", `https://hashkey.blockscout.com/address/${address}`);

  const out = {
    contract: "ScratchWalletRegistry",
    address,
    deployTx: tx.hash,
    chainId: Number(network.chainId),
    rpc: process.env.HASHKEY_RPC_URL || "https://mainnet.hsk.xyz",
    explorer: `https://hashkey.blockscout.com/address/${address}`,
    deployedAt: new Date().toISOString()
  };
  writeDeploymentHelpers(out, deployer.address);
  console.log("Wrote deployment/hashkey.json");
  console.log("Wrote deployment/.env.deployed.example");
  console.log("Wrote deployment/streamlit_secrets.toml");
  console.log("Next: copy SCRATCH_REGISTRY_ADDRESS into .env or Streamlit secrets.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
