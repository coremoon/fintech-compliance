"""
Example: Analyze a blockchain project for compliance

This example shows how to use the BlockchainComplianceAgent to assess
a Bitcoin/Simplicity project against EU regulations.

Phase 4: This will work once Phase 2 (Agent) is complete
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.blockchain_compliance_agent.agent import BlockchainComplianceAgent

def main():
    """Example: Analyze Bitcoin Staking Pool"""
    
    # Initialize agent
    agent = BlockchainComplianceAgent()
    
    # Your project description
    project = """
    Bitcoin Staking Pool with Simplicity Contracts
    
    TECHNICAL:
    - Smart contracts written in Simplicity (on Taproot)
    - Users deposit BTC (custodied in HSM with 2-of-3 multisig)
    - Pool algorithm selects staking operators (using ML: XGBoost model)
    - Rewards distributed via Lightning Network
    - KYC data: Name, Email, Wallet Address (encrypted PostgreSQL)
    - Fee: 2% of rewards (calculated in Simplicity contract)
    
    BUSINESS:
    - Target: EU-based users
    - Go-live: Q2 2025
    - Expected AUM: €5-10M Year 1
    
    QUESTIONS:
    1. Do we need MiFID2 license?
    2. What are GDPR requirements for HSM + KYC storage?
    3. Is our ML model "high-risk AI" under EU AI Act?
    4. If contract bugs → who is liable?
    """
    
    # Run analysis
    result = agent.analyze_project(project)
    
    # Print results
    print("\n" + "="*70)
    print("COMPLIANCE ANALYSIS REPORT")
    print("="*70)
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
