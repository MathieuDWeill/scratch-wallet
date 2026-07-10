from .models import Opportunity

DANGEROUS_APPROVALS = {"unlimited_approval", "setApprovalForAll", "permit_phishing"}


def inspect_claim(opportunity: Opportunity) -> dict:
    if opportunity.approval_request in DANGEROUS_APPROVALS:
        return {
            "safe": False,
            "risk": "CRITICAL",
            "assets_at_risk": ["ERC-20 balances", "future wallet approvals", "campaign wallet bankroll"],
            "finding": "The claim asks for a permission unrelated to receiving free tokens.",
            "recommendation": "Do not sign. Skip and record as rug dodged.",
        }
    if opportunity.kind == "safe_claim" and opportunity.verified_contract:
        return {
            "safe": True,
            "risk": "LOW",
            "assets_at_risk": [],
            "finding": "No approval or external transfer permission detected in the mock call.",
            "recommendation": "Safe enough for the selected risk mode, subject to bankroll rules.",
        }
    return {
        "safe": False,
        "risk": "UNKNOWN",
        "assets_at_risk": ["unknown"],
        "finding": "Claim could not be classified safely.",
        "recommendation": "Skip by default.",
    }
