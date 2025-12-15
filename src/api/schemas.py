"""
Pydantic Models for API Request/Response Validation

Defines all input and output schemas for REST endpoints.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class BusinessModelEnum(str, Enum):
    """Crypto business model types."""
    CASP = "CASP"
    DEX = "DEX"
    STAKING = "STAKING"
    LENDING = "LENDING"
    WALLET = "WALLET"
    OTHER = "OTHER"


class LanguageEnum(str, Enum):
    """Smart contract languages."""
    SIMPLICITY = "simplicity"
    BITCOIN_SCRIPT = "bitcoin_script"
    OTHER = "other"


class RiskLevelEnum(str, Enum):
    """Risk assessment levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class ProjectAnalysisRequest(BaseModel):
    """Request to analyze a blockchain/crypto project."""
    
    project_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the project"
    )
    
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Project description"
    )
    
    business_model: BusinessModelEnum = Field(
        ...,
        description="Type of crypto business"
    )
    
    target_jurisdiction: str = Field(
        default="EU",
        description="Target jurisdiction (e.g., EU, USA, Global)"
    )
    
    specific_regulations: Optional[List[str]] = Field(
        default=None,
        description="Specific regulations to focus on (e.g., GDPR, MICA)"
    )
    
    class ConfigDict:
        example = {
            "project_name": "MyBitcoinStakingApp",
            "description": "Bitcoin staking service allowing users to earn yield...",
            "business_model": "STAKING",
            "target_jurisdiction": "EU",
            "specific_regulations": ["MICA", "GDPR", "MiFID2"]
        }


class ContractAnalysisRequest(BaseModel):
    """Request to analyze a smart contract."""
    
    contract_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the contract"
    )
    
    source_code: str = Field(
        ...,
        min_length=10,
        description="Smart contract source code"
    )
    
    language: LanguageEnum = Field(
        default=LanguageEnum.SIMPLICITY,
        description="Contract language"
    )
    
    witness_data: Optional[str] = Field(
        default=None,
        description="Witness data (JSON format for Simplicity-HL)"
    )
    
    class ConfigDict:
        example = {
            "contract_name": "MultiSigWallet",
            "source_code": "fn main() { ... }",
            "language": "simplicity",
            "witness_data": "{...}"
        }


class RegulationSearchRequest(BaseModel):
    """Request to search regulations."""
    
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Search query"
    )
    
    regulations: Optional[List[str]] = Field(
        default=None,
        description="Filter by regulations (e.g., GDPR, MICA)"
    )
    
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum results to return"
    )
    
    class ConfigDict:
        example = {
            "query": "custody requirements",
            "regulations": ["MICA", "GDPR"],
            "limit": 10
        }


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class ComplianceRisk(BaseModel):
    """A single compliance risk."""
    
    regulation: str
    risk: str
    description: str
    severity: RiskLevelEnum
    mitigation: str


class Recommendation(BaseModel):
    """A single recommendation."""
    
    priority: int
    category: str
    description: str
    estimated_effort: Optional[str] = None


class AnalysisResult(BaseModel):
    """Generic analysis result container."""
    
    status: str
    message: Optional[str] = None
    data: Dict[str, Any]
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None


class ProjectAnalysisResponse(BaseModel):
    """Response from project analysis."""
    
    status: str = Field(description="success or error")
    project_name: str
    analysis: Dict[str, Any] = Field(description="Full analysis results")
    regulations_applicable: List[str]
    risk_level: RiskLevelEnum
    critical_issues: List[str]
    compliance_roadmap: List[Dict[str, Any]]
    tokens_used: int
    cost_usd: float
    
    class ConfigDict:
        example = {
            "status": "success",
            "project_name": "MyBitcoinStakingApp",
            "risk_level": "MEDIUM",
            "tokens_used": 2500,
            "cost_usd": 0.15
        }


class CompilationResult(BaseModel):
    """Smart contract compilation result."""
    
    status: str  # "success" or "error"
    message: Optional[str] = None
    bytecode: Optional[str] = None
    bytecode_size: Optional[int] = None
    has_error: bool = False
    error_type: Optional[str] = None


class PatternDetection(BaseModel):
    """Detected smart contract pattern."""
    
    pattern: str
    description: str
    risk_level: RiskLevelEnum
    count: int


class ContractAnalysisResponse(BaseModel):
    """Response from contract analysis."""
    
    status: str = Field(description="success or error")
    contract_name: str
    compilation: CompilationResult
    patterns_detected: List[PatternDetection]
    complexity_level: str  # LOW, MEDIUM, HIGH
    security_concerns: List[Dict[str, str]]
    compliance_risks: List[ComplianceRisk]
    recommendations: List[Recommendation]
    claude_assessment: Optional[str] = None
    tokens_used: int


class SearchResult(BaseModel):
    """Single search result."""
    
    id: str
    regulation: str
    article: Optional[str] = None
    title: str
    content: str
    relevance_score: float
    enforcement_cases: Optional[List[Dict[str, str]]] = None


class RegulationSearchResponse(BaseModel):
    """Response from regulation search."""
    
    status: str
    query: str
    results_count: int
    results: List[SearchResult]
    search_time_ms: float


class RegulationDetailResponse(BaseModel):
    """Detailed information about a regulation."""
    
    status: str
    id: str
    regulation: str
    title: str
    article: Optional[str] = None
    content: str
    full_text: Optional[str] = None
    enforcement_cases: List[Dict[str, Any]]
    related_articles: List[str]
    compliance_tips: List[str]


class EnforcementCase(BaseModel):
    """Single enforcement case."""
    
    company: str
    regulator: str
    violation: str
    fine: str
    date: str
    jurisdiction: str
    key_lesson: str
    link: Optional[str] = None


class EnforcementCasesResponse(BaseModel):
    """Response from enforcement cases query."""
    
    status: str
    total_cases: int
    cases: List[EnforcementCase]
    filters_applied: Dict[str, str]


class HealthCheckResponse(BaseModel):
    """API health check response."""
    
    status: str  # "healthy" or "degraded"
    services: Dict[str, str]
    timestamp: str
    uptime_seconds: float
    version: str


class ErrorResponse(BaseModel):
    """Error response."""
    
    status: str = "error"
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@field_validator("query")
def validate_query(cls, v):
    """Validate search query."""
    if len(v.strip()) < 3:
        raise ValueError("Query must be at least 3 characters")
    return v.strip()


@field_validator("source_code")
def validate_code(cls, v):
    """Validate smart contract code."""
    if len(v.strip()) < 10:
        raise ValueError("Code must be at least 10 characters")
    return v.strip()
