"""
Example: Claude + Weaviate Integration (v4)

Shows how to use Claude to analyze data from Weaviate.

Run:
  python examples/test_claude_weaviate.py
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.data.weaviate import Weaviate
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage

# Load config
load_dotenv()

print("=" * 70)
print("  Claude + Weaviate Integration Example (v4)")
print("=" * 70)
print()

# Initialize
w = Weaviate()
w.create_schema()

print("Step 1: Add sample enforcement cases to Weaviate")
print("-" * 70)

# Add sample cases
cases = [
    {
        "company": "Revolut",
        "violation": "GDPR - Insufficient data protection measures",
        "fine": 1000000,
        "articles": ["GDPR Art. 5", "GDPR Art. 32"],
        "year": 2018,
        "lessons": ["Implement encryption", "Regular security audits"]
    },
    {
        "company": "Celsius Network",
        "violation": "SEC - Unregistered securities offering",
        "fine": 50000000,
        "articles": ["Securities Act"],
        "year": 2023,
        "lessons": ["Classify products correctly", "Get proper licensing"]
    },
    {
        "company": "Kraken",
        "violation": "CFTC - Unregistered staking as derivatives",
        "fine": 30000000,
        "articles": ["CEA", "CFTC Regulations"],
        "year": 2023,
        "lessons": ["Staking may be derivatives", "Comply with CFTC"]
    }
]

for case in cases:
    w.add_case(**case)
    print(f"✅ Added: {case['company']}")

print()

# Get all cases
print("Step 2: Retrieve cases from Weaviate")
print("-" * 70)

all_cases = w.get_all_cases()
print(f"✅ Found {len(all_cases)} cases in Weaviate")
print()

# Format for Claude
print("Step 3: Ask Claude to analyze cases")
print("-" * 70)

case_text = "\n".join([
    f"• {c['company']} ({c['year']}): {c['violation']} (Fine: ${c['fine']:,.0f})"
    for c in all_cases
])

prompt = f"""
Analyze these crypto/fintech enforcement cases:

{case_text}

What are the top 3 compliance lessons for a new blockchain project?
Be concise (max 3 bullets).
"""

print(f"Prompt to Claude:")
print(prompt)
print()

# Call Claude
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

claude = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0.1)
response = claude.invoke([HumanMessage(content=prompt)])

print("Claude's Response:")
print("-" * 70)
print(response.content)
print()

print("=" * 70)
print("✅ Integration working!")
print("=" * 70)
print()

print("""
WHAT JUST HAPPENED:

1. Weaviate stored 3 enforcement cases
2. We retrieved all cases from Weaviate
3. We formatted the data
4. Claude analyzed the data
5. Got intelligent compliance insights

THIS IS YOUR AGENT FOUNDATION:

In Week 1, you'll:
- Populate Weaviate with 10-20 real cases
- Add EU regulations
- Create tools that search Weaviate
- Have Claude reason about the results

Then in Week 2:
- Expose via REST API
- Test against your Bitcoin project
- Done!
""")

w.close()
