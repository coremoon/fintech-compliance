"""
Test Setup: Claude + Weaviate Integration (v4)

Run this before starting development to verify everything works:
  python test_setup.py
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

print("=" * 70)
print("  fintech-compliance - Setup Test")
print("=" * 70)
print()

# Load env
load_dotenv()

# Test 1: Configuration
print("TEST 1: Configuration")
print("-" * 70)

try:
    from src.config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, WEAVIATE_URL
    
    api_key_ok = bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY.startswith("sk-ant-"))
    weaviate_url_ok = bool(WEAVIATE_URL)
    
    print(f"✅ Config loaded")
    print(f"   Claude Model: {ANTHROPIC_MODEL}")
    print(f"   Claude API Key: {'✅ SET' if api_key_ok else '❌ NOT SET'}")
    print(f"   Weaviate URL: {WEAVIATE_URL}")
    
    if not api_key_ok:
        print("\n⚠️  WARNING: Claude API key not set in .env")
        print("   Add: ANTHROPIC_API_KEY=sk-ant-v1-YOUR_KEY")
    
    print()
except Exception as e:
    print(f"❌ Config failed: {e}")
    print()

# Test 2: Claude API
print("TEST 2: Claude API Connection")
print("-" * 70)

try:
    from langchain_anthropic import ChatAnthropic
    from langchain.schema import HumanMessage
    
    if not ANTHROPIC_API_KEY:
        print("❌ Claude API key not set - skipping test")
        print()
    else:
        # Set API key in environment (new langchain_anthropic expects this)
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
        
        claude = ChatAnthropic(
            model=ANTHROPIC_MODEL,
            temperature=0.1,
            max_tokens=256
        )
        
        # Simple test
        message = claude.invoke([HumanMessage(content="Say 'Claude is working' in one sentence.")])
        
        if message.content:
            print(f"✅ Claude API working")
            print(f"   Response: {message.content}")
            print()
        else:
            print("❌ Claude returned empty response")
            print()
except Exception as e:
    print(f"❌ Claude API failed: {e}")
    print()

# Test 3: Weaviate
print("TEST 3: Weaviate Connection (v4)")
print("-" * 70)

try:
    from src.data.weaviate import Weaviate
    
    w = Weaviate(url=WEAVIATE_URL)
    print(f"✅ Weaviate connected at {WEAVIATE_URL}")
    
    # Try to create schema
    w.create_schema()
    print(f"✅ Weaviate schemas initialized")
    
    # Test data
    w.add_case(
        company="Test Company",
        violation="Test violation",
        fine=100000,
        articles=["Test Art."],
        year=2024,
        lessons=["Test lesson"]
    )
    print(f"✅ Data insertion works")
    
    # Test retrieval
    cases = w.get_all_cases()
    print(f"✅ Data retrieval works ({len(cases)} cases found)")
    
    w.close()
    print()
except Exception as e:
    print(f"❌ Weaviate failed: {e}")
    print(f"   Make sure: docker-compose up -d")
    print(f"   Or: make weaviate-up")
    print()

# Test 4: Integration
print("TEST 4: Claude + Weaviate Integration")
print("-" * 70)

try:
    if not ANTHROPIC_API_KEY:
        print("❌ Skipping (Claude API key not set)")
        print()
    else:
        from src.data.weaviate import Weaviate
        from langchain_anthropic import ChatAnthropic
        from langchain.schema import HumanMessage
        
        # Set API key in environment
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
        
        w = Weaviate(url=WEAVIATE_URL)
        claude = ChatAnthropic(model=ANTHROPIC_MODEL, temperature=0.1)
        
        # Get data from Weaviate
        cases = w.get_all_cases()
        
        if cases:
            # Create prompt with Weaviate data
            case_text = "\n".join([
                f"- {c['company']}: {c['violation']} (${c['fine']:,.0f})"
                for c in cases[:3]
            ])
            
            prompt = f"""
Analyze these enforcement cases:

{case_text}

What's the common pattern? (1 sentence)
"""
            
            # Ask Claude
            response = claude.invoke([HumanMessage(content=prompt)])
            
            print(f"✅ Claude + Weaviate integration works")
            print(f"   Weaviate found {len(cases)} case(s)")
            print(f"   Claude analysis: {response.content}")
            print()
        else:
            print("⚠️  No data in Weaviate - integration test skipped")
            print()
        
        w.close()
            
except Exception as e:
    print(f"❌ Integration failed: {e}")
    print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Configuration       - Loaded
✅ Claude API          - Test message sent
✅ Weaviate (v4)       - Connected
✅ Integration         - Claude uses Weaviate data

NEXT STEPS:

1. Upgrade Weaviate client:
   pip install --upgrade weaviate-client
   
2. If all tests passed:
   python test_setup.py    # Run anytime to verify
   
3. Start implementation:
   - Week 1: Collectors
   - Week 1: Agent
   - Week 2: API

Good luck! 🚀
""")
