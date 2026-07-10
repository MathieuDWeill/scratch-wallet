// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title ScratchWalletRegistry
/// @notice Audit registry for Scratch Wallet decisions on HashKey Chain.
/// @dev The contract does not custody funds and does not execute trades. It anchors signed/off-chain
///      decisions so an autonomous micro-wallet can be reviewed after the fact.
contract ScratchWalletRegistry {
    struct Decision {
        uint256 id;
        address reporter;
        address scratchWallet;
        bytes32 opportunityHash;
        bytes32 decisionTypeHash;
        bytes32 riskModeHash;
        uint256 startingBankroll; // scaled by 1e6 for USDC-style display in the app
        uint256 tradeSize;        // scaled by 1e6
        int256 grossEdgeBps;
        int256 netEdgeBps;
        uint256 riskScore;        // 0-100
        bool played;
        bytes32 reportHash;
        uint256 createdAt;
        string reportURI;
    }

    uint256 public nextDecisionId = 1;
    mapping(uint256 => Decision) public decisions;
    mapping(address => uint256[]) private decisionsByWallet;
    mapping(bytes32 => uint256[]) private decisionsByOpportunity;

    event ScratchDecisionAnchored(
        uint256 indexed id,
        address indexed reporter,
        address indexed scratchWallet,
        bool played,
        bytes32 opportunityHash,
        bytes32 reportHash
    );
    event OpportunityPlayed(uint256 indexed id, address indexed scratchWallet, int256 netEdgeBps);
    event OpportunitySkipped(uint256 indexed id, address indexed scratchWallet, uint256 riskScore);
    event ScratchWalletStopped(address indexed scratchWallet, bytes32 indexed reportHash, string reason);
    event RugDodged(address indexed scratchWallet, bytes32 indexed opportunityHash, bytes32 reportHash);

    function anchorDecision(
        address scratchWallet,
        bytes32 opportunityHash,
        bytes32 decisionTypeHash,
        bytes32 riskModeHash,
        uint256 startingBankroll,
        uint256 tradeSize,
        int256 grossEdgeBps,
        int256 netEdgeBps,
        uint256 riskScore,
        bool played,
        bytes32 reportHash,
        string calldata reportURI
    ) public returns (uint256 id) {
        require(scratchWallet != address(0), "scratch wallet required");
        require(riskScore <= 100, "risk score out of range");
        require(reportHash != bytes32(0), "report hash required");

        id = nextDecisionId++;
        decisions[id] = Decision({
            id: id,
            reporter: msg.sender,
            scratchWallet: scratchWallet,
            opportunityHash: opportunityHash,
            decisionTypeHash: decisionTypeHash,
            riskModeHash: riskModeHash,
            startingBankroll: startingBankroll,
            tradeSize: tradeSize,
            grossEdgeBps: grossEdgeBps,
            netEdgeBps: netEdgeBps,
            riskScore: riskScore,
            played: played,
            reportHash: reportHash,
            createdAt: block.timestamp,
            reportURI: reportURI
        });
        decisionsByWallet[scratchWallet].push(id);
        decisionsByOpportunity[opportunityHash].push(id);

        emit ScratchDecisionAnchored(id, msg.sender, scratchWallet, played, opportunityHash, reportHash);
        if (played) emit OpportunityPlayed(id, scratchWallet, netEdgeBps);
        else emit OpportunitySkipped(id, scratchWallet, riskScore);
    }

    function anchorSkippedOpportunity(
        address scratchWallet,
        bytes32 opportunityHash,
        bytes32 riskModeHash,
        uint256 riskScore,
        bytes32 reportHash,
        string calldata reportURI
    ) external returns (uint256 id) {
        return anchorDecision(
            scratchWallet,
            opportunityHash,
            keccak256(abi.encodePacked("SKIP")),
            riskModeHash,
            0,
            0,
            0,
            0,
            riskScore,
            false,
            reportHash,
            reportURI
        );
    }

    function anchorWalletStopped(address scratchWallet, bytes32 reportHash, string calldata reason) external {
        require(scratchWallet != address(0), "scratch wallet required");
        require(reportHash != bytes32(0), "report hash required");
        emit ScratchWalletStopped(scratchWallet, reportHash, reason);
    }

    function anchorRugDodged(address scratchWallet, bytes32 opportunityHash, bytes32 reportHash) external {
        require(scratchWallet != address(0), "scratch wallet required");
        require(reportHash != bytes32(0), "report hash required");
        emit RugDodged(scratchWallet, opportunityHash, reportHash);
    }

    function getDecision(uint256 id) external view returns (Decision memory) {
        return decisions[id];
    }

    function getDecisionsByWallet(address wallet) external view returns (uint256[] memory) {
        return decisionsByWallet[wallet];
    }

    function getDecisionsByOpportunity(bytes32 opportunityHash) external view returns (uint256[] memory) {
        return decisionsByOpportunity[opportunityHash];
    }
}
