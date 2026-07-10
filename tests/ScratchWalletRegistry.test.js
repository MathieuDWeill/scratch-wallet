const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ScratchWalletRegistry", function () {
  it("anchors a played decision", async function () {
    const [owner, wallet] = await ethers.getSigners();
    const Factory = await ethers.getContractFactory("ScratchWalletRegistry");
    const registry = await Factory.deploy();
    await registry.waitForDeployment();

    const reportHash = ethers.keccak256(ethers.toUtf8Bytes("report"));
    const opportunityHash = ethers.keccak256(ethers.toUtf8Bytes("opportunity"));
    const tx = await registry.anchorDecision(
      wallet.address,
      opportunityHash,
      ethers.keccak256(ethers.toUtf8Bytes("PLAY")),
      ethers.keccak256(ethers.toUtf8Bytes("Normal")),
      100_000000,
      10_000000,
      42,
      11,
      24,
      true,
      reportHash,
      "ipfs://demo"
    );
    await expect(tx).to.emit(registry, "ScratchDecisionAnchored");
    const d = await registry.getDecision(1);
    expect(d.reporter).to.equal(owner.address);
    expect(d.scratchWallet).to.equal(wallet.address);
    expect(d.played).to.equal(true);
  });
});
