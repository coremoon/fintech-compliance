"""
Example: Using Fintech Compliance API with Python
CORRECTED VERSION - All field names match actual API schemas
"""

import requests
import json
from typing import Dict, Any

import sys
from pathlib import Path


# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import API_PORT

# API Base URL
API_BASE = f"http://localhost:{API_PORT}/api/v1"

# ============================================================================
# 1. HEALTH CHECK
# ============================================================================

def check_health() -> Dict[str, Any]:
    """Check if API is running"""
    response = requests.get(f"{API_BASE}/health")
    response.raise_for_status()
    return response.json()


# ============================================================================
# 2. ANALYZE PROJECT
# ============================================================================

def analyze_project(
    project_name: str,
    description: str,
    business_model: str,
    target_jurisdiction: str,
    specific_regulations: list
) -> Dict[str, Any]:
    """Analyze blockchain project for compliance"""
    
    payload = {
        "project_name": project_name,
        "description": description,
        "business_model": business_model,
        "target_jurisdiction": target_jurisdiction,
        "specific_regulations": specific_regulations
    }
    
    response = requests.post(
        f"{API_BASE}/analyze/project",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


# ============================================================================
# 3. ANALYZE SMART CONTRACT
# ============================================================================

def analyze_contract(
    source_code: str,
    language: str,
    contract_name: str,
    witness_data: str = None
) -> Dict[str, Any]:
    """Analyze smart contract"""
    
    payload = {
        "source_code": source_code,
        "language": language,
        "contract_name": contract_name,
        "witness_data": witness_data
    }
    
    response = requests.post(
        f"{API_BASE}/analyze/contract",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


# ============================================================================
# 4. SEARCH REGULATIONS
# ============================================================================

def search_regulations(
    query: str,
    regulations: list = None,
    limit: int = 10
) -> Dict[str, Any]:
    """Search regulations and enforcement cases"""
    
    payload = {
        "query": query,
        "regulations": regulations,
        "limit": limit
    }
    
    response = requests.post(
        f"{API_BASE}/regulations/search",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("🚀 FINTECH COMPLIANCE API CLIENT\n")
    print("=" * 70)
    
    # 1. Health Check
    print("\n1️⃣  HEALTH CHECK")
    print("-" * 70)
    try:
        health = check_health()
        print(f"✅ Status: {health['status']}")
        print(f"✅ Uptime: {health['uptime_seconds']:.1f}s")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Analyze Project
    print("\n2️⃣  ANALYZE PROJECT")
    print("-" * 70)
    try:
        analysis = analyze_project(
            project_name="Bitcoin Staking Protocol",
            description="Native Bitcoin staking with Simplicity contracts",
            business_model="STAKING",
            target_jurisdiction="EU",
            specific_regulations=["MICA", "GDPR"]
        )
        print(f"✅ Project: {analysis['project_name']}")
        print(f"✅ Risk Level: {analysis['risk_level']}")
        print(f"✅ Regulations: {analysis['regulations_applicable']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Analyze Contract
    print("\n3️⃣  ANALYZE SMART CONTRACT")
    print("-" * 70)
    try:
        contract_analysis = analyze_contract(
            source_code="""
            fn stake(amount: i64) -> bool {
                assert!(amount > 0, "Amount must be positive");
                deposit(amount);
                true
            }
            """,
            language="simplicity",
            contract_name="StakingPool"
        )
        print(f"✅ Contract: {contract_analysis['contract_name']}")
        print(f"✅ Complexity: {contract_analysis.get('complexity_level', 'N/A')}")
        print(f"✅ Tokens Used: {contract_analysis.get('tokens_used', 'N/A')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Search Regulations
    print("\n4️⃣  SEARCH REGULATIONS")
    print("-" * 70)
    try:
        search_results = search_regulations(
            query="staking rewards regulatory requirements",
            regulations=["GDPR"],
            limit=10
        )
        print(f"✅ Query: {search_results['query']}")
        print(f"✅ Results: {search_results['results_count']}")
        print(f"✅ Search Time: {search_results['search_time_ms']}ms")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETE\n")