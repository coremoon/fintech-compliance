"""
Simplicity Smart Contract Analyzer

Analyzes:
- Contract code structure and patterns
- Covenant and timelock mechanisms
- Asset-backing implementations
- Custody and escrow logic
- Compliance risk factors
- Compilation with pysimplicityhl
"""

import re
import json
import tempfile
import os
from typing import List, Dict, Any, Tuple
from src.utils.logger import logger

try:
    import pysimplicityhl
    PYSIMPLICITYHL_AVAILABLE = True
except ImportError:
    PYSIMPLICITYHL_AVAILABLE = False


class SimplicitContractAnalyzer:
    """Analyzer for Simplicity smart contracts"""
    
    # Common contract patterns to detect
    PATTERNS = {
        "covenant": {
            "regex": r"(checklocktimeverify|cltv|sequence|timelock|OP_CLTV|OP_CSV)",
            "description": "Covenant mechanism",
            "risk_level": "high"
        },
        "multisig": {
            "regex": r"(multisig|m_of_n|OP_CHECKMULTISIG|threshold|checkmultisig)",
            "description": "Multi-signature requirement",
            "risk_level": "medium"
        },
        "custody": {
            "regex": r"(custody|custodian|wallet|key_management|segregate|hsm)",
            "description": "Custodial mechanism",
            "risk_level": "high"
        },
        "oracle": {
            "regex": r"(oracle|attestation|signature|verify|external_data|feed)",
            "description": "Oracle integration",
            "risk_level": "medium"
        },
        "yield": {
            "regex": r"(yield|staking|reward|return|dividend|interest|payout)",
            "description": "Yield generation mechanism",
            "risk_level": "high"
        },
        "escrow": {
            "regex": r"(escrow|dispute|release|condition|atomic|swap|htlc)",
            "description": "Escrow mechanism",
            "risk_level": "medium"
        },
        "asset_backing": {
            "regex": r"(asset|backing|reserve|collateral|commodity|proof_of_reserves)",
            "description": "Asset-backing mechanism",
            "risk_level": "high"
        },
        "emergency": {
            "regex": r"(emergency|pause|halt|stop|shutdown|recovery|failsafe)",
            "description": "Emergency control mechanism",
            "risk_level": "medium"
        }
    }
    
    def __init__(self):
        """Initialize contract analyzer"""
        pass
    
    def compile_contract(self, code: str) -> Dict[str, Any]:
        """
        Compile Simplicity contract using pysimplicityhl
        
        Args:
            code: Simplicity contract source code
        
        Returns:
            Compilation result with status, bytecode, size, etc.
        """
        
        if not PYSIMPLICITYHL_AVAILABLE:
            return {
                "status": "error",
                "message": "pysimplicityhl not available. Install: pip install pysimplicityhl"
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.simpl',
            delete=False
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Compile with pysimplicityhl
            result_json = pysimplicityhl.run_from_python(temp_file)
            result = json.loads(result_json)
            
            # Extract compilation info
            compilation_info = {
                "status": result.get("status", "unknown"),
                "message": result.get("message", ""),
                "has_error": result.get("status") == "error"
            }
            
            # If successful, try to extract additional info
            if result.get("status") == "success":
                # Try to get bytecode info from result
                if "bytecode" in result:
                    compilation_info["bytecode"] = result["bytecode"]
                    compilation_info["bytecode_size"] = len(result["bytecode"]) // 2
                
                if "ast" in result:
                    compilation_info["has_ast"] = True
                
                compilation_info["compiled"] = True
            else:
                compilation_info["compiled"] = False
                # Extract error details
                if "Grammar error" in compilation_info["message"]:
                    compilation_info["error_type"] = "Grammar error"
                elif "Type error" in compilation_info["message"]:
                    compilation_info["error_type"] = "Type error"
                else:
                    compilation_info["error_type"] = "Compilation error"
            
            return compilation_info
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Compilation exception: {str(e)}",
                "error_type": "Exception",
                "compiled": False
            }
        
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def analyze_contract(self, contract_code: str, 
                        contract_name: str = "Unknown") -> Dict[str, Any]:
        """
        Analyze a Simplicity contract
        
        Args:
            contract_code: Simplicity contract source code
            contract_name: Name of the contract
        
        Returns:
            Analysis results including compilation info
        """
        
        analysis = {
            "contract_name": contract_name,
            "code_size": len(contract_code),
            "line_count": len(contract_code.split('\n')),
            "patterns_detected": [],
            "security_concerns": [],
            "compliance_risks": [],
            "recommendations": [],
            "compilation": {}
        }
        
        # Compile with pysimplicityhl
        compilation_result = self.compile_contract(contract_code)
        analysis["compilation"] = compilation_result
        
        # Detect patterns
        patterns = self._detect_patterns(contract_code)
        analysis["patterns_detected"] = patterns
        
        # Assess complexity
        complexity = self._assess_complexity(contract_code)
        analysis["complexity"] = complexity
        
        # Check for security issues
        security_issues = self._check_security_issues(contract_code)
        analysis["security_concerns"] = security_issues
        
        # Identify compliance risks
        compliance_risks = self._identify_compliance_risks(patterns, contract_code)
        analysis["compliance_risks"] = compliance_risks
        
        # Generate recommendations
        recommendations = self._generate_recommendations(patterns, compliance_risks)
        analysis["recommendations"] = recommendations
        
        return analysis
    
    def _detect_patterns(self, code: str) -> List[Dict[str, Any]]:
        """
        Detect contract patterns
        
        Args:
            code: Contract code
        
        Returns:
            List of detected patterns
        """
        
        detected = []
        
        for pattern_name, pattern_info in self.PATTERNS.items():
            if re.search(pattern_info["regex"], code, re.IGNORECASE):
                detected.append({
                    "pattern": pattern_name,
                    "description": pattern_info["description"],
                    "risk_level": pattern_info["risk_level"]
                })
        
        return detected
    
    def _assess_complexity(self, code: str) -> Dict[str, Any]:
        """
        Assess contract complexity
        
        Args:
            code: Contract code
        
        Returns:
            Complexity assessment
        """
        
        lines = code.split('\n')
        
        # Count functions/definitions
        functions = len(re.findall(r'(fn |def |function )', code, re.IGNORECASE))
        
        # Count conditionals
        conditionals = len(re.findall(r'(if |case |match )', code, re.IGNORECASE))
        
        # Count loops
        loops = len(re.findall(r'(while |for |loop )', code, re.IGNORECASE))
        
        # Determine complexity level
        total_complexity = functions + conditionals + loops
        
        if total_complexity < 5:
            level = "low"
        elif total_complexity < 15:
            level = "medium"
        else:
            level = "high"
        
        return {
            "level": level,
            "functions": functions,
            "conditionals": conditionals,
            "loops": loops,
            "total_score": total_complexity
        }
    
    def _check_security_issues(self, code: str) -> List[Dict[str, Any]]:
        """
        Check for common security issues
        
        Args:
            code: Contract code
        
        Returns:
            List of security concerns
        """
        
        issues = []
        
        # Check for hardcoded values
        if re.search(r'(0x[0-9a-f]{32,}|hardcoded|magic_number)', code, re.IGNORECASE):
            issues.append({
                "issue": "Potential hardcoded values",
                "severity": "medium",
                "description": "Hardcoded values may indicate inflexibility or security issues",
                "recommendation": "Review and parameterize hardcoded values"
            })
        
        # Check for insufficient validation
        if not re.search(r'(validate|verify|assert|require|check)', code, re.IGNORECASE):
            issues.append({
                "issue": "Insufficient input validation",
                "severity": "high",
                "description": "No apparent validation of inputs",
                "recommendation": "Add comprehensive input validation"
            })
        
        # Check for missing access controls
        if not re.search(r'(permission|auth|access_control|owner|role)', code, re.IGNORECASE):
            issues.append({
                "issue": "Missing access controls",
                "severity": "high",
                "description": "No apparent authorization mechanism",
                "recommendation": "Implement role-based access control"
            })
        
        # Check for reentrancy vulnerabilities (common in custody)
        if "custody" in code.lower() or "wallet" in code.lower():
            if not re.search(r'(mutex|lock|guard|reentrancy_guard)', code, re.IGNORECASE):
                issues.append({
                    "issue": "Potential reentrancy vulnerability in custody code",
                    "severity": "critical",
                    "description": "Custody code without reentrancy protection",
                    "recommendation": "Implement reentrancy guards for all external calls"
                })
        
        return issues
    
    def _identify_compliance_risks(self, patterns: List[Dict[str, Any]], 
                                   code: str) -> List[Dict[str, Any]]:
        """
        Identify regulatory compliance risks
        
        Args:
            patterns: Detected patterns
            code: Contract code
        
        Returns:
            List of compliance risks
        """
        
        risks = []
        pattern_names = [p["pattern"] for p in patterns]
        
        # Asset-backing risks
        if "asset_backing" in pattern_names:
            risks.append({
                "regulation": "MICA",
                "risk": "Asset classification and authorization",
                "description": "Asset-backed tokens require MICA authorization",
                "severity": "critical",
                "mitigation": "Obtain CASP authorization before deployment"
            })
            risks.append({
                "regulation": "GDPR",
                "risk": "Reserve attestation and oracle data",
                "description": "Oracle data may contain personal information",
                "severity": "medium",
                "mitigation": "Ensure GDPR compliance for attestation mechanisms"
            })
        
        # Custody risks
        if "custody" in pattern_names:
            risks.append({
                "regulation": "MICA",
                "risk": "Customer asset segregation requirement",
                "description": "MICA requires strict segregation of customer funds",
                "severity": "critical",
                "mitigation": "Implement segregated accounts and insurance"
            })
            risks.append({
                "regulation": "GDPR",
                "risk": "Private key management",
                "description": "Key storage may violate data minimization principles",
                "severity": "high",
                "mitigation": "Consider non-custodial alternatives"
            })
        
        # Yield generation risks
        if "yield" in pattern_names:
            risks.append({
                "regulation": "MICA/MiFID2",
                "risk": "Promised returns on crypto-assets",
                "description": "Fixed yield promises may trigger investment service classification",
                "severity": "critical",
                "mitigation": "Obtain investment service authorization if applicable"
            })
            risks.append({
                "regulation": "MICA",
                "risk": "Unregistered staking services",
                "description": "Staking services require CASP authorization",
                "severity": "critical",
                "mitigation": "Obtain CASP authorization for staking services"
            })
        
        # Oracle risks
        if "oracle" in pattern_names:
            risks.append({
                "regulation": "Market Manipulation/Price Integrity",
                "risk": "Oracle manipulation vulnerability",
                "description": "Single-source oracles are vulnerable to manipulation",
                "severity": "high",
                "mitigation": "Use decentralized oracle networks with multiple sources"
            })
        
        # Timelock/covenant risks
        if "covenant" in pattern_names:
            risks.append({
                "regulation": "Dispute Resolution",
                "risk": "Dispute period and customer protection",
                "description": "Timelocks may prevent timely dispute resolution",
                "severity": "medium",
                "mitigation": "Ensure adequate dispute resolution timeframes"
            })
        
        # Escrow risks
        if "escrow" in pattern_names:
            risks.append({
                "regulation": "AML/CFT",
                "risk": "Cross-border transaction monitoring",
                "description": "Escrow mechanisms must comply with AML/CFT rules",
                "severity": "high",
                "mitigation": "Implement transaction monitoring and STR reporting"
            })
        
        return risks
    
    def _generate_recommendations(self, patterns: List[Dict[str, Any]], 
                                 risks: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommendations
        
        Args:
            patterns: Detected patterns
            risks: Identified risks
        
        Returns:
            List of recommendations
        """
        
        recommendations = []
        pattern_names = [p["pattern"] for p in patterns]
        
        # Critical compliance recommendations
        critical_risks = [r for r in risks if r["severity"] == "critical"]
        
        if critical_risks:
            recommendations.append(
                f"CRITICAL: Address {len(critical_risks)} critical compliance risks before deployment"
            )
        
        # Pattern-specific recommendations
        if "custody" in pattern_names:
            recommendations.append(
                "Implement multi-signature custody with key distribution to separate entities"
            )
            recommendations.append(
                "Obtain MICA CASP authorization for custodial services"
            )
            recommendations.append(
                "Implement customer asset segregation with insurance/guarantee"
            )
        
        if "yield" in pattern_names:
            recommendations.append(
                "Conduct investment service classification analysis (MiFID2)"
            )
            recommendations.append(
                "If classified as investment service, obtain authorization"
            )
            recommendations.append(
                "Clearly disclose risks and variable return nature"
            )
        
        if "asset_backing" in pattern_names:
            recommendations.append(
                "Implement regular proof-of-reserves mechanism"
            )
            recommendations.append(
                "Use multi-source oracle attestation for reserve verification"
            )
            recommendations.append(
                "Define asset redemption procedures in contract code"
            )
        
        if "oracle" in pattern_names:
            recommendations.append(
                "Implement decentralized oracle network (not single-source)"
            )
            recommendations.append(
                "Include circuit-breaker for extreme price movements"
            )
        
        if "covenant" in pattern_names:
            recommendations.append(
                "Document all timelocks and their business purpose"
            )
            recommendations.append(
                "Ensure timelocks allow adequate dispute resolution periods"
            )
        
        # General recommendations
        if len(patterns) > 5:
            recommendations.append(
                "High contract complexity detected - conduct formal security audit"
            )
        
        recommendations.append(
            "Engage legal counsel for final regulatory classification"
        )
        
        return recommendations
    
    def format_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """
        Format analysis as readable report
        
        Args:
            analysis: Analysis results
        
        Returns:
            Formatted report text
        """
        
        report = f"""
CONTRACT ANALYSIS REPORT
========================

Contract: {analysis['contract_name']}
Code Size: {analysis['code_size']} bytes
Lines: {analysis['line_count']}

PATTERNS DETECTED ({len(analysis['patterns_detected'])}):
"""
        
        for pattern in analysis['patterns_detected']:
            report += f"- {pattern['pattern']}: {pattern['description']} (Risk: {pattern['risk_level']})\n"
        
        report += f"\nCOMPLEXITY: {analysis['complexity']['level'].upper()}\n"
        report += f"  Functions: {analysis['complexity']['functions']}\n"
        report += f"  Conditionals: {analysis['complexity']['conditionals']}\n"
        report += f"  Loops: {analysis['complexity']['loops']}\n"
        
        if analysis['security_concerns']:
            report += f"\nSECURITY CONCERNS ({len(analysis['security_concerns'])}):\n"
            for concern in analysis['security_concerns']:
                report += f"- [{concern['severity'].upper()}] {concern['issue']}\n"
                report += f"  → {concern['recommendation']}\n"
        
        if analysis['compliance_risks']:
            report += f"\nCOMPLIANCE RISKS ({len(analysis['compliance_risks'])}):\n"
            for risk in analysis['compliance_risks']:
                report += f"- [{risk['severity'].upper()}] {risk['regulation']}: {risk['risk']}\n"
                report += f"  → {risk['mitigation']}\n"
        
        if analysis['recommendations']:
            report += f"\nRECOMMENDATIONS ({len(analysis['recommendations'])}):\n"
            for i, rec in enumerate(analysis['recommendations'], 1):
                report += f"{i}. {rec}\n"
        
        return report


def main():
    """Test the analyzer"""
    
    # Example contract
    example_contract = """
    # Asset-backed token on Bitcoin using Simplicity
    
    contract AssetBackedToken {
        # Multisig custody for reserves
        fn custody_verify(signatures) -> bool {
            checkmultisig(2, 3)  # 2-of-3 required
        }
        
        # Timelock for dispute resolution
        fn dispute_period(time) -> bool {
            checklocktimeverify(time)
        }
        
        # Oracle attestation for reserves
        fn verify_reserves(oracle_signature) -> bool {
            verify_oracle_signature(oracle_signature)
        }
        
        # Yield distribution
        fn distribute_yield(amount, recipients) -> bool {
            for recipient in recipients {
                release_funds(recipient, amount)
            }
        }
    }
    """
    
    analyzer = SimplicitContractAnalyzer()
    analysis = analyzer.analyze_contract(
        example_contract,
        "AssetBackedToken"
    )
    
    report = analyzer.format_analysis_report(analysis)
    print(report)


if __name__ == "__main__":
    main()
