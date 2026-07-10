require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

const HASHKEY_RPC_URL = process.env.HASHKEY_RPC_URL || "https://mainnet.hsk.xyz";
const DEPLOYER_PRIVATE_KEY = process.env.DEPLOYER_PRIVATE_KEY || process.env.ANCHOR_PRIVATE_KEY || "";

module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      viaIR: true
    }
  },
  networks: {
    hardhat: {},
    hashkey: {
      url: HASHKEY_RPC_URL,
      chainId: Number(process.env.HASHKEY_CHAIN_ID || 177),
      accounts: DEPLOYER_PRIVATE_KEY ? [DEPLOYER_PRIVATE_KEY] : []
    }
  },
  paths: {
    sources: "./contracts",
    tests: "./tests",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  etherscan: {
    apiKey: {
      hashkey: process.env.BLOCKSCOUT_API_KEY || "no-api-key-needed"
    },
    customChains: [
      {
        network: "hashkey",
        chainId: Number(process.env.HASHKEY_CHAIN_ID || 177),
        urls: {
          apiURL: "https://hashkey.blockscout.com/api",
          browserURL: "https://hashkey.blockscout.com"
        }
      }
    ]
  }
};
