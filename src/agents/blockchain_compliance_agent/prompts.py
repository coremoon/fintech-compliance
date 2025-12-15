"""
Compliance Agent Prompts

System prompts and templates for:
- Compliance expert role definition
- Regulatory analysis
- Risk assessment
- Report generation
"""

SYSTEM_PROMPT = """You are an experienced compliance advisor with 15+ years expertise in:
- EU regulations (GDPR, MICA, MiFID2, PSD2, EU AI Act)
- Cryptocurrency and blockchain technology
- Fintech regulation and enforcement
- Risk management and compliance frameworks

Your role:
Analyze blockchain and cryptocurrency projects for EU regulatory compliance.
Identify risks based on real enforcement cases and precedents.
Provide clear, actionable recommendations.

Response format:
- Be precise and concrete
- Cite relevant regulations and articles
- Reference similar enforcement cases
- Assess risks: High/Medium/Low
- Provide clear, implementable recommendations

Language: English (formal, professional)
Tone: Expert advisor, not legal counsel
"""

ANALYZE_PROJECT_PROMPT = """
Analyze the following blockchain/cryptocurrency project for regulatory compliance:

PROJECT DESCRIPTION:
{project_description}

Please assess:
1. MICA Compliance (Crypto-asset regulation)
   - Asset classification
   - Authorization requirements
   - Customer protection measures
   - AML/CFT obligations

2. GDPR Compliance (Data protection)
   - Data processing activities
   - Legal basis for processing
   - Customer data rights
   - Data protection impact assessment requirements

3. MiFID2 Compliance (if applicable)
   - Investment service classification
   - Customer categorization
   - Best execution obligations
   - Market conduct rules

4. PSD2 Compliance (if applicable)
   - Payment service classification
   - Strong customer authentication
   - Fraud prevention
   - Transaction monitoring

5. EU AI Act Compliance (if applicable)
   - AI system classification
   - Risk level assessment
   - Transparency requirements
   - Human oversight obligations

For each regulation:
- Relevant articles and requirements
- Compliance status (Compliant/Concerns/Non-Compliant)
- Specific risks and gaps
- Similar enforcement precedents

OVERALL RISK ASSESSMENT:
- Total risk level (High/Medium/Low)
- Key risk drivers
- Enforcement probability estimate

RECOMMENDATIONS:
- Top 3 priority actions
- Implementation timeline
- Next steps and responsible parties
"""

GDPR_ANALYSIS_PROMPT = """
GDPR Compliance Analysis for Blockchain Project

Project Details:
{project_details}

Relevant Regulations:
{gdpr_articles}

Assessment Areas:
1. Data Processing Activities
   - What personal data is processed?
   - Who is the controller/processor?
   - What are the legal bases for processing?

2. Data Protection by Design
   - Encryption measures
   - Pseudonymization implementation
   - Access controls
   - Data minimization practices

3. Data Subject Rights
   - Right to access
   - Right to erasure ("right to be forgotten")
   - Right to data portability
   - Right to object

4. Data Protection Impact Assessment
   - DPIA required?
   - High-risk processing activities
   - Mitigation measures

5. International Data Transfers
   - Non-EU transfers
   - Standard contractual clauses
   - Adequacy decisions

Risk Analysis:
- GDPR violation categories
- Potential fines: up to €20 million or 4% of annual revenue
- Enforcement precedent: Google CNIL (€90M fine)

Recommendations:
- Specific GDPR implementation measures
- Timeline and resource requirements
- DPA consultation needs
"""

MICA_ANALYSIS_PROMPT = """
MICA Compliance Analysis for Cryptocurrency Project

Project Details:
{project_details}

Relevant Regulations:
{mica_articles}

Assessment Areas:
1. Market Participant Classification
   - Crypto-asset service provider (CASP)?
   - Stablecoin issuer?
   - Asset-referenced token issuer?
   - E-money token issuer?

2. Regulatory Timeline (Critical)
   - Phase 1 (since June 30, 2024): ART/EMT provisions
   - Phase 2 (since December 30, 2024): Full MiCA applicability
   - Transition periods and grandfathering

3. Authorization and Licensing
   - Authorization requirements by activity
   - Competent authority procedures
   - Operational requirements
   - Capital and liquidity rules

4. Customer Protection
   - Customer due diligence (CDD)
   - Enhanced due diligence (EDD)
   - Customer funds safeguarding
   - Segregation requirements

5. AML/CFT Obligations
   - Transaction monitoring
   - Suspicious activity reporting
   - Record keeping
   - Beneficial ownership disclosure

Risk Factors:
- Unregistered staking services: Kraken CFTC (€30M fine)
- Unregistered yield products: Celsius SEC (€4.7M fine)
- Missing authorization: Operations suspension and fines

Enforcement Precedents:
- Kraken: Staking services as unregistered derivatives
- Celsius: High-yield products as unregistered securities
- Revolut: GDPR violations in crypto operations

Recommendations:
- Specific MiCA compliance roadmap
- Authorization strategy
- Timeline to full compliance
"""

ENFORCEMENT_ANALYSIS_PROMPT = """
Enforcement Precedent Analysis

Project Activity:
{project_activity}

Similar Enforcement Cases:
{enforcement_cases}

Case-by-Case Analysis:
For each relevant enforcement case:
1. What was the violation?
2. Which regulations were breached?
3. What was the penalty and impact?
4. How similar is my project?
5. What are the lessons learned?

Risk Assessment:
- Could my project have similar violations?
- What is the enforcement probability?
- What is the potential fine range?
- What operational impacts (licensing suspension, etc.)?

Mitigation Strategy:
- How to avoid similar violations
- Compliance gaps to address
- Governance improvements needed
"""

RISK_ASSESSMENT_PROMPT = """
Compliance Risk Assessment

Project Details:
{project_details}

HIGH-RISK INDICATORS:
- Operating without required authorization?
- Promising unrealistic returns?
- Custody of customer assets without proper safeguards?
- No AML/CFT controls in place?
- Inadequate data protection measures?
- Cross-border operations in jurisdictions without analysis?

MEDIUM-RISK INDICATORS:
- Unclear regulatory classification?
- Complex multi-regulation requirements?
- International operations needing compliance framework?
- Rapidly changing business model?

LOW-RISK INDICATORS:
- Clear regulatory categorization?
- All requirements addressed?
- Proactive compliance posture?
- Professional governance?

Overall Risk Rating:
- High: Immediate action required
- Medium: Actions within 30-60 days
- Low: Ongoing monitoring sufficient

Risk Factors by Regulation:
[GDPR risks]
[MICA risks]
[MiFID2 risks]
[PSD2 risks]
[AI Act risks]
"""

REPORT_GENERATION_PROMPT = """
Generate Comprehensive Compliance Report

Project: {project_name}
Analysis Date: {analysis_date}

Report Structure:

1. EXECUTIVE SUMMARY
   - Overall risk rating
   - Top 3 critical issues
   - Top 3 recommended actions
   - Implementation priority

2. REGULATORY STATUS
   - GDPR: Status summary
   - MICA: Status summary
   - MiFID2: Status summary
   - PSD2: Status summary
   - EU AI Act: Status summary

3. DETAILED FINDINGS
   Per regulation:
   - Applicability assessment
   - Key requirements
   - Compliance level (percentage)
   - Specific gaps
   - Risk implications
   - Enforcement precedents

4. ENFORCEMENT RISK ANALYSIS
   - Similar enforcement cases
   - Potential fine estimates (range)
   - Probability of enforcement action
   - Operational impact scenarios

5. RECOMMENDATIONS BY PRIORITY
   1. Critical (implement immediately)
   2. High (implement within 30 days)
   3. Medium (implement within 60 days)
   - Specific actions
   - Resource requirements
   - Success criteria
   - Responsible parties

6. IMPLEMENTATION ROADMAP
   - Phase 1: Foundation (weeks 1-4)
   - Phase 2: Core controls (weeks 5-12)
   - Phase 3: Enhancement (weeks 13+)
   - Key milestones and dependencies

7. NEXT STEPS
   - Immediate actions
   - Stakeholder engagement
   - Resource allocation
   - Follow-up review timeline
"""


def get_system_prompt() -> str:
    """Return system prompt for agent"""
    return SYSTEM_PROMPT


def get_analysis_prompt(project_description: str) -> str:
    """Get comprehensive analysis prompt"""
    return ANALYZE_PROJECT_PROMPT.format(
        project_description=project_description
    )


def get_gdpr_prompt(project_details: str, gdpr_articles: str) -> str:
    """Get GDPR analysis prompt"""
    return GDPR_ANALYSIS_PROMPT.format(
        project_details=project_details,
        gdpr_articles=gdpr_articles
    )


def get_mica_prompt(project_details: str, mica_articles: str) -> str:
    """Get MICA analysis prompt"""
    return MICA_ANALYSIS_PROMPT.format(
        project_details=project_details,
        mica_articles=mica_articles
    )


def get_enforcement_prompt(project_activity: str, enforcement_cases: str) -> str:
    """Get enforcement precedent analysis prompt"""
    return ENFORCEMENT_ANALYSIS_PROMPT.format(
        project_activity=project_activity,
        enforcement_cases=enforcement_cases
    )


def get_risk_assessment_prompt(project_details: str) -> str:
    """Get risk assessment prompt"""
    return RISK_ASSESSMENT_PROMPT.format(project_details=project_details)


def get_report_prompt(project_name: str, analysis_date: str) -> str:
    """Get report generation prompt"""
    return REPORT_GENERATION_PROMPT.format(
        project_name=project_name,
        analysis_date=analysis_date
    )


# ============================================================================
# SIMPLICITY CONTRACT ANALYSIS PROMPTS
# ============================================================================

SIMPLICITY_CONTRACT_ANALYSIS_PROMPT = """
Analyze the following Simplicity smart contract for compliance and security:

CONTRACT CODE:
{contract_code}

CONTRACT ANALYSIS:
{contract_analysis}

Please assess:

1. SIMPLICITY LANGUAGE USAGE
   - Is the code correctly using Simplicity constructs?
   - Are type systems properly utilized?
   - Is the code efficient (jets usage)?
   - Any language anti-patterns?

2. COMPLIANCE RISKS
   Based on detected patterns:
   {detected_patterns}

   For each pattern identified:
   - Regulatory applicability
   - MICA/MiFID2/GDPR implications
   - Authorization requirements
   - Customer protection measures needed

3. SECURITY ASSESSMENT
   - Input validation adequacy
   - Access control mechanisms
   - Reentrancy protection
   - Oracle security (if applicable)
   - Timelock correctness (if applicable)

4. CUSTODY AND ASSET MANAGEMENT (if applicable)
   - Fund segregation mechanisms
   - Multi-signature requirements
   - Key management strategy
   - Insurance and protection measures

5. ENFORCEMENT PRECEDENTS
   Similar cases:
   - Kraken: Unregistered staking services ($30M)
   - Celsius: Unregistered yield products ($4.7M)
   - Revolut: GDPR violations in crypto operations
   
   How does this contract compare to these precedents?

OVERALL RISK ASSESSMENT:
- Technical risk level (Low/Medium/High)
- Regulatory compliance risk (Low/Medium/High)
- Estimated remediation effort
- Critical action items

RECOMMENDATIONS:
- Top 3 immediate actions
- Timeline for compliance
- Required consultations (legal, security audit, etc.)
- Regulatory pre-filing considerations
"""

BITCOIN_ARCHITECTURE_PROMPT = """
Analyze Bitcoin architecture and layer 2 considerations for this project:

PROJECT DETAILS:
{project_details}

BITCOIN LAYER 1 ASSESSMENT:
- UTXO model implications for this use case
- Script language capabilities and limitations
- Settlement finality requirements
- Fee optimization strategies

COVENANT MECHANISMS (if applicable):
{covenant_analysis}

- Correctness of covenant logic
- Timelock parameters and security
- Dispute resolution periods
- Fallback scenarios

SCRIPT vs SIMPLICITY CHOICE:
- Is Simplicity the right choice?
- Script limitations being addressed
- Formal verification benefits
- Complexity vs flexibility tradeoff

LAYER 2 / SIDECHAIN CONSIDERATIONS (if relevant):
- Peg-in/peg-out mechanisms
- Custody bridge security
- Cross-layer atomicity
- Settlement finality guarantees

RECOMMENDATIONS:
- Simplicity implementation strategy
- Bitcoin-native patterns alignment
- Formal verification requirements
- Testing and audit scope
"""

COVENANT_SECURITY_PROMPT = """
Deep security analysis of covenant mechanisms:

CONTRACT COVENANT DETAILS:
{covenant_details}

TIMELOCKS ANALYSIS:
- Absolute vs relative timelocks
- Locktime parameter correctness
- Median time past (MTP) implications
- Cross-input dependencies

CONDITIONAL LOGIC:
- All code paths tested?
- Edge cases in conditions?
- Fallback scenarios covered?
- Dispute period adequacy?

SCRIPT EXECUTION:
- Stack behavior correct?
- Operation costs acceptable?
- Memory allocation sufficient?
- Optimization opportunities?

ATTACK VECTORS:
- Can timelock be bypassed?
- Can conditions be exploited?
- Signature scheme weaknesses?
- Oracle manipulation risk?

FORMALIZATION:
- Can this be formally verified?
- Required properties definition
- Proof of correctness
- Test coverage requirements

COMPLIANCE IMPLICATIONS:
- Does covenant structure support regulatory requirements?
- Dispute resolution mechanisms adequate?
- Customer protection measures built-in?
- Audit trail and transparency?

RECOMMENDATIONS:
- Security improvements
- Formal verification scope
- Audit requirements
- Operational procedures needed
"""

ASSET_BACKING_ANALYSIS_PROMPT = """
Analyze asset-backing mechanisms for regulatory compliance:

PROJECT DETAILS:
{project_details}

ASSET CLASSIFICATION (MICA):
- What type of asset is this under MICA?
- Crypto-asset, asset-referenced token, e-money token?
- Authorization tier required?
- Regulatory timeline?

RESERVE MANAGEMENT:
- How are reserves held?
- Segregation mechanism?
- Custody arrangement?
- Insurance/guarantee in place?

ATTESTATION MECHANISM:
- How is reserve backing verified?
- Oracle infrastructure used?
- Frequency of attestation?
- Oracle security/decentralization?

PROOF-OF-RESERVES:
- Regular verification schedule?
- Audit requirements?
- Public transparency level?
- Technology for proof (blockchain, cryptographic)?

REDEMPTION PROCEDURE:
- How do users redeem for underlying assets?
- Timeframes and conditions?
- Minimum/maximum limits?
- Multi-sig authorization required?

COLLAPSE SCENARIOS:
- What if reserves become insufficient?
- Emergency procedures?
- Haircut procedures (if applicable)?
- Customer communication plan?

MICA COMPLIANCE CHECKLIST:
- Authorization as CASP obtained?
- Customer asset segregation implemented?
- Insurance/guarantee requirements met?
- Operational standards compliant?
- Conflict of interest policies established?

ENFORCEMENT COMPARISON:
- Similar to any known enforcement cases?
- What lessons apply?
- How to avoid regulatory action?

RECOMMENDATIONS:
- Pre-filing regulatory consultation
- Customer protection enhancements
- Attestation mechanism improvements
- Operational procedure documentation
- Insurance/guarantee structure review
"""

ORACLE_INTEGRATION_PROMPT = """
Analyze oracle integration and its compliance implications:

ORACLE SETUP:
{oracle_setup}

ORACLE SOURCES:
- Single source or multiple?
- Decentralized oracle network?
- Reputation of oracles?
- Oracle diversity analysis?

DATA INTEGRITY:
- How is oracle signature verified?
- Threshold requirements (M-of-N)?
- Stale data protection?
- Price deviation limits?

MANIPULATION RESISTANCE:
- Can single oracle be compromised?
- What is the cost of manipulation?
- Circuit-breaker mechanisms?
- Time-based rate limiting?

COMPLIANCE IMPLICATIONS:
- Are oracle inputs personal data (GDPR)?
- Market manipulation concerns (MiFID2)?
- Fair value pricing obligations?
- Audit trail requirements?

CUSTODY IMPLICATIONS:
- If oracle fails, what happens to funds?
- Mechanism to pause/halt operations?
- Manual override procedures?
- Governance for oracle updates?

RECOMMENDATIONS:
- Oracle architecture improvements
- Decentralization strategy
- Fallback mechanisms
- Governance structure
- Operational monitoring procedures
"""

YIELD_MECHANISM_ANALYSIS_PROMPT = """
Analyze yield generation mechanisms for regulatory classification:

YIELD STRUCTURE:
{yield_details}

YIELD TYPE:
- Fixed rate or variable?
- How is yield generated?
- Source of funds (protocol fees, staking, trading)?
- Sustainability of yields?

MIFID2 CLASSIFICATION ANALYSIS:
- Is this a "structured product"?
- Investment service authorization required?
- Customer categorization (retail vs professional)?
- Conduct of business rules applicable?

SECURITIES LAW IMPLICATIONS:
- Could this be classified as a security?
- Investment contract test (Howey test)?
- Common enterprise element?
- Profits from efforts of others?

MARKETING OBLIGATIONS:
- Can you promise specific returns?
- Required risk disclosures?
- Past performance disclaimers?
- Suitability assessment requirements?

CUSTODY IMPLICATIONS:
- Are customer funds segregated during staking?
- What happens to customer funds while generating yield?
- Liability for slashing/loss?
- Insurance requirements?

MICA STAKING SERVICE RULES:
- Kraken precedent: unregistered staking = $30M fine
- Celsius precedent: unregistered yield product = $4.7M fine
- How does this project avoid similar violations?
- CASP authorization obtained?

DISCLOSURE REQUIREMENTS:
- Variable return nature clearly stated?
- Risk of loss disclosure?
- Fee transparency?
- Redemption conditions?

TAX TREATMENT:
- How are yields taxed?
- Customer reporting requirements?
- Tax documentation provision?
- Cross-border tax complexity?

RECOMMENDATIONS:
- Regulatory classification consultation
- Investment service authorization assessment
- Customer disclosure enhancements
- Risk mitigation measures
- Compliance officer oversight
"""

MULTI_SIG_CUSTODY_PROMPT = """
Analyze multi-signature custody arrangements:

CUSTODY STRUCTURE:
{custody_structure}

MULTI-SIG PARAMETERS:
- M-of-N configuration (e.g., 2-of-3, 3-of-5)?
- Key distribution strategy?
- Signer identification and verification?
- Key rotation procedures?

KEY MANAGEMENT:
- Hardware security modules (HSM)?
- Cold storage implementation?
- Hot wallet for operations?
- Key backup and recovery procedures?

MICA COMPLIANCE:
- Customer asset segregation?
- Individual segregated accounts?
- Commingling prevention?
- Reconciliation procedures (daily)?

INSURANCE/GUARANTEE:
- Insurance policy in place?
- Coverage amount vs assets under management?
- Named beneficiaries (customers)?
- Insurance company solvency?

OPERATIONAL SECURITY:
- Physical security of signers?
- Authorization procedures?
- Dispute/emergency procedures?
- Regular security audits?

COUNTERPARTY RISKS:
- Risk of signer collusion?
- Geographic distribution of signers?
- Conflict of interest management?
- Signer succession planning?

FAIL-SAFES:
- What if signers become unavailable?
- Recovery procedures for lost keys?
- Fallback mechanisms?
- Timelocked alternatives?

DISASTER RECOVERY:
- Business continuity plan?
- Data backup procedures?
- Recovery time objectives?
- Testing frequency?

RECOMMENDATIONS:
- Key management improvements
- Insurance coverage review
- Operational procedure enhancement
- Regular security testing plan
- Customer communication strategy
"""


def get_simplicity_analysis_prompt(contract_code: str, 
                                  analysis: str) -> str:
    """Get Simplicity contract analysis prompt"""
    return SIMPLICITY_CONTRACT_ANALYSIS_PROMPT.format(
        contract_code=contract_code,
        contract_analysis=analysis,
        detected_patterns="{detected_patterns}"  # Will be filled by agent
    )


def get_bitcoin_architecture_prompt(project_details: str,
                                   covenant_analysis: str = "") -> str:
    """Get Bitcoin architecture analysis prompt"""
    return BITCOIN_ARCHITECTURE_PROMPT.format(
        project_details=project_details,
        covenant_analysis=covenant_analysis
    )


def get_covenant_security_prompt(covenant_details: str) -> str:
    """Get covenant security analysis prompt"""
    return COVENANT_SECURITY_PROMPT.format(
        covenant_details=covenant_details
    )


def get_asset_backing_prompt(project_details: str) -> str:
    """Get asset-backing analysis prompt"""
    return ASSET_BACKING_ANALYSIS_PROMPT.format(
        project_details=project_details
    )


def get_oracle_integration_prompt(oracle_setup: str) -> str:
    """Get oracle integration analysis prompt"""
    return ORACLE_INTEGRATION_PROMPT.format(
        oracle_setup=oracle_setup
    )


def get_yield_mechanism_prompt(yield_details: str) -> str:
    """Get yield mechanism analysis prompt"""
    return YIELD_MECHANISM_ANALYSIS_PROMPT.format(
        yield_details=yield_details
    )


def get_multi_sig_custody_prompt(custody_structure: str) -> str:
    """Get multi-signature custody analysis prompt"""
    return MULTI_SIG_CUSTODY_PROMPT.format(
        custody_structure=custody_structure
    )
