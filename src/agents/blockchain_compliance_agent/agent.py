"""
Blockchain Compliance Agent

Orchestrates:
- Weaviate search (tools)
- Claude API reasoning
- System prompts
- Report generation
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agents.blockchain_compliance_agent.tools import ComplianceTools
from src.agents.blockchain_compliance_agent import prompts
from src.utils.logger import logger

try:
    import anthropic
except ImportError:
    logger.error("anthropic library not found. Install: pip install anthropic")
    sys.exit(1)


class BlockchainComplianceAgent:
    """AI-powered compliance advisor for blockchain and cryptocurrency projects"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize compliance agent
        
        Args:
            api_key: Claude API key (or from ANTHROPIC_API_KEY environment variable)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.tools = ComplianceTools()
        self.model = "claude-sonnet-4-5-20250929"
        self.max_tokens = 4096
    
    def analyze_project(self, project_description: str, 
                       project_name: str = "Unnamed Project") -> Dict[str, Any]:
        """
        Analyze project for regulatory compliance
        
        Args:
            project_description: Description of the project
            project_name: Name of the project
        
        Returns:
            Dictionary with compliance analysis and recommendations
        """
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🔍 COMPLIANCE ANALYSIS: {project_name}")
        logger.info(f"{'='*80}\n")
        
        # Step 1: Identify relevant regulations
        logger.info("📋 Step 1: Regulatory coverage analysis...")
        relevant_regs = self.tools.analyze_regulation_coverage(project_description)
        
        regs_summary = "\n".join([
            f"- {reg}: {data['count']} relevant articles"
            for reg, data in relevant_regs.items()
        ])
        
        logger.info(f"   Relevant regulations:\n{regs_summary}\n")
        
        # Step 2: Retrieve enforcement cases
        logger.info("📋 Step 2: Enforcement precedent analysis...")
        enforcement_cases = self.tools.get_enforcement_cases()
        
        cases_summary = "\n".join([
            f"- {case.get('title', 'Unknown')}"
            for case in enforcement_cases[:5]
        ])
        
        logger.info(f"   Enforcement cases:\n{cases_summary}\n")
        
        # Step 3: Claude analysis with prompt engineering
        logger.info("🤖 Step 3: Claude analysis with specialized prompts...\n")
        
        analysis_prompt = prompts.get_analysis_prompt(project_description)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=prompts.get_system_prompt(),
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )
            
            analysis_text = response.content[0].text
            
            # Display token counts
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # Calculate costs (Sonnet 4.5 pricing)
            input_cost = (input_tokens / 1_000_000) * 3.00      # $3/1M input tokens
            output_cost = (output_tokens / 1_000_000) * 15.00   # $15/1M output tokens
            total_cost = input_cost + output_cost
            
            logger.info(f"\n{'='*80}")
            logger.info(f"📊 TOKEN USAGE & COSTS")
            logger.info(f"{'='*80}")
            logger.info(f"Input Tokens:   {input_tokens:,}")
            logger.info(f"Output Tokens:  {output_tokens:,}")
            logger.info(f"Total Tokens:   {total_tokens:,}")
            logger.info(f"\nCost Breakdown:")
            logger.info(f"  Input:  ${input_cost:.4f}")
            logger.info(f"  Output: ${output_cost:.4f}")
            logger.info(f"  Total:  ${total_cost:.4f}")
            logger.info(f"{'='*80}\n")
            
            logger.info("✅ Analysis completed!\n")
            
            return {
                "project_name": project_name,
                "analysis_date": datetime.now().isoformat(),
                "relevant_regulations": relevant_regs,
                "enforcement_cases": enforcement_cases[:3],
                "analysis": analysis_text,
                "raw_response": response,
                "token_usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "cost": {
                        "input": input_cost,
                        "output": output_cost,
                        "total": total_cost
                    }
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Claude API error: {e}")
            return {
                "error": str(e),
                "project_name": project_name
            }
    
    def quick_check(self, question: str) -> str:
        """
        Ask quick compliance question
        
        Args:
            question: Compliance question
        
        Returns:
            Agent response
        """
        
        logger.info(f"\n❓ Question: {question}\n")
        
        # Search relevant regulations
        relevant_regs = self.tools.search_regulations(question)
        
        context = f"""
Relevant regulations on this topic:
{json.dumps([r.get('title') for r in relevant_regs[:3]], ensure_ascii=False)}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=prompts.get_system_prompt(),
                messages=[
                    {
                        "role": "user",
                        "content": f"{context}\n\nQuestion: {question}"
                    }
                ]
            )
            
            answer = response.content[0].text
            
            # Display token counts
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # Calculate costs
            input_cost = (input_tokens / 1_000_000) * 3.00
            output_cost = (output_tokens / 1_000_000) * 15.00
            total_cost = input_cost + output_cost
            
            logger.info(f"✅ Answer:\n{answer}\n")
            logger.info(f"Tokens: {total_tokens} (${total_cost:.4f})\n")
            return answer
        
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return f"Error: {e}"
    
    def analyze(self, project_description: str, project_name: str = "Unnamed Project"):
        """
        Test-compatible wrapper for analyze_project
        """
        return self.analyze_project(
            project_description=project_description,
            project_name=project_name
        )

    def generate_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate compliance report from analysis
        
        Args:
            analysis_result: Result from analyze_project()
        
        Returns:
            Formatted compliance report
        """
        
        if "error" in analysis_result:
            return f"❌ Report generation failed: {analysis_result['error']}"
        
        logger.info(f"\n{'='*80}")
        logger.info(f"📄 COMPLIANCE REPORT: {analysis_result['project_name']}")
        logger.info(f"{'='*80}\n")
        
        report = f"""
COMPLIANCE REPORT
=================

Project: {analysis_result['project_name']}
Date: {analysis_result['analysis_date']}

ANALYSIS:
---------
{analysis_result['analysis']}

RELEVANT REGULATIONS:
---------------------
"""
        
        for reg, data in analysis_result['relevant_regulations'].items():
            report += f"\n{reg}: {data['count']} articles\n"
        
        report += "\nENFORCEMENT PRECEDENTS:\n----------------------\n"
        
        for case in analysis_result['enforcement_cases']:
            report += f"\n- {case.get('title', 'Unknown')}\n"
        
        logger.info(report)
        return report


def main():
    """Interactive CLI interface for agent"""
    
    print("\n" + "="*80)
    print("🤖 BLOCKCHAIN COMPLIANCE ADVISOR")
    print("="*80 + "\n")
    
    # Initialize agent
    try:
        agent = BlockchainComplianceAgent()
        print("✅ Agent initialized\n")
    except Exception as e:
        print(f"❌ Agent initialization error: {e}")
        sys.exit(1)
    
    # Interactive loop
    while True:
        print("\n" + "-"*80)
        print("MENU:")
        print("1. Analyze project")
        print("2. Ask compliance question")
        print("3. Search regulations")
        print("4. View enforcement cases")
        print("5. Exit")
        print("-"*80)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\n📝 PROJECT ANALYSIS")
            name = input("Project name: ").strip()
            print("Project description (press Enter twice to finish):")
            lines = []
            empty_count = 0
            while True:
                line = input()
                if not line:
                    empty_count += 1
                    if empty_count >= 1:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            
            description = "\n".join(lines)
            if not description:
                print("❌ Empty description")
                continue
            
            result = agent.analyze_project(description, name)
            agent.generate_report(result)
        
        elif choice == "2":
            print("\n❓ COMPLIANCE QUESTION")
            question = input("Ask your question: ").strip()
            if question:
                agent.quick_check(question)
        
        elif choice == "3":
            print("\n📋 SEARCH REGULATIONS")
            query = input("Search term: ").strip()
            if query:
                results = agent.tools.search_regulations(query)
                print(f"\n✅ {len(results)} articles found:\n")
                for i, r in enumerate(results[:5], 1):
                    print(f"{i}. {r.get('title', 'Unknown')}")
                    print(f"   Regulation: {r.get('regulation', '')}\n")
        
        elif choice == "4":
            print("\n📋 ENFORCEMENT CASES")
            cases = agent.tools.get_enforcement_cases()
            print(f"\n✅ {len(cases)} cases available:\n")
            for i, case in enumerate(cases[:5], 1):
                print(f"{i}. {case.get('title', 'Unknown')}")
                print(f"   {case.get('regulation', '')}\n")
        
        elif choice == "5":
            print("\n✅ Goodbye!\n")
            break
        
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
