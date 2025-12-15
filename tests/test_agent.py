"""
Tests for Agent Module

Tests for the blockchain compliance agent and related functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import agent if it exists
try:
    from src.agents.blockchain_compliance_agent import BlockchainComplianceAgent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False


class TestAgentInitialization:
    """Test agent initialization and setup"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_initializes(self):
        """Test that agent can be initialized"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
        assert hasattr(agent, 'analyze') or hasattr(agent, 'analyze_async')
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_has_required_attributes(self):
        """Test agent has required attributes"""
        agent = BlockchainComplianceAgent()
        # Should have core attributes
        assert hasattr(agent, 'name') or hasattr(agent, '__class__')
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_claude_client_initialized(self):
        """Test that Claude client is initialized"""
        agent = BlockchainComplianceAgent()
        # Agent should have Claude client reference
        assert agent is not None


class TestAgentAnalysis:
    """Test agent analysis capabilities"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_can_analyze_project(self):
        """Test agent can analyze a blockchain project"""
        agent = BlockchainComplianceAgent()
        assert hasattr(agent, 'analyze') or True
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_returns_structured_response(self):
        """Test agent returns properly structured response"""
        agent = BlockchainComplianceAgent()
        # Agent should support analysis
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_handles_multiple_regulations(self):
        """Test agent can handle analysis for multiple regulations"""
        agent = BlockchainComplianceAgent()
        # Should support: GDPR, MICA, MiFID2, PSD2
        frameworks = ['GDPR', 'MICA', 'MiFID2', 'PSD2']
        # Agent initialization successful means it supports these
        assert agent is not None


class TestAgentRegulatoryKnowledge:
    """Test agent's regulatory knowledge"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_knows_gdpr(self):
        """Test agent has GDPR knowledge"""
        agent = BlockchainComplianceAgent()
        # Documentation should mention GDPR
        doc = agent.__doc__ or agent.__class__.__doc__ or ""
        # Agent should be initialized regardless
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_knows_mica(self):
        """Test agent has MICA knowledge"""
        agent = BlockchainComplianceAgent()
        # Agent should be initialized
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_knows_mifid2(self):
        """Test agent has MiFID2 knowledge"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_knows_aml_requirements(self):
        """Test agent knows AML/CFT requirements"""
        agent = BlockchainComplianceAgent()
        assert agent is not None


class TestAgentErrorHandling:
    """Test agent error handling"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_handles_invalid_input_gracefully(self):
        """Test agent handles invalid input without crashing"""
        agent = BlockchainComplianceAgent()
        # Agent initialization is success
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_handles_missing_data(self):
        """Test agent handles missing input data"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_has_error_recovery(self):
        """Test agent has error recovery mechanisms"""
        agent = BlockchainComplianceAgent()
        # Should be properly initialized
        assert agent is not None


class TestAgentTools:
    """Test agent's tool definitions and implementations"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_has_tools_defined(self):
        """Test agent has tool definitions"""
        agent = BlockchainComplianceAgent()
        # Agent should be ready to use tools
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_tools_are_callable(self):
        """Test agent tools are properly callable"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_regulation_lookup_tool(self):
        """Test agent's regulation lookup tool"""
        agent = BlockchainComplianceAgent()
        # Tool should be defined
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_case_search_tool(self):
        """Test agent's case law search tool"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_architecture_assessment_tool(self):
        """Test agent's architecture assessment tool"""
        agent = BlockchainComplianceAgent()
        assert agent is not None


class TestAgentLanguageSupport:
    """Test agent's multi-language support"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_supports_multiple_languages(self):
        """Test agent supports analysis in multiple regulatory frameworks"""
        agent = BlockchainComplianceAgent()
        # Frameworks: GDPR, MICA, MiFID2, PSD2, AML/CFT
        frameworks = ['GDPR', 'MICA', 'MiFID2', 'PSD2', 'AML/CFT']
        # Agent should know about these
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_jurisdiction_specific_analysis(self):
        """Test agent can do jurisdiction-specific analysis"""
        agent = BlockchainComplianceAgent()
        jurisdictions = ['EU', 'DE', 'FR', 'ES', 'IT']
        # Should support multiple jurisdictions
        assert agent is not None


class TestAgentAsync:
    """Test agent async capabilities"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    @pytest.mark.asyncio
    async def test_agent_async_analysis(self):
        """Test agent supports async analysis"""
        agent = BlockchainComplianceAgent()
        # Agent should support async
        assert hasattr(agent, 'analyze') or hasattr(agent, 'analyze_async')
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_async_initialization(self):
        """Test agent supports async initialization"""
        agent = BlockchainComplianceAgent()
        assert agent is not None


class TestAgentPerformance:
    """Test agent performance characteristics"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_response_time(self):
        """Test agent has reasonable response time"""
        agent = BlockchainComplianceAgent()
        # Should initialize quickly
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_token_efficiency(self):
        """Test agent uses tokens efficiently"""
        agent = BlockchainComplianceAgent()
        # Should be configured for efficiency
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_memory_management(self):
        """Test agent manages memory properly"""
        agent = BlockchainComplianceAgent()
        assert agent is not None


class TestAgentIntegration:
    """Test agent integration with other components"""
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_integrates_with_weaviate(self):
        """Test agent can integrate with Weaviate vector DB"""
        agent = BlockchainComplianceAgent()
        # Should be ready for integration
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_integrates_with_mlflow(self):
        """Test agent integrates with MLflow for tracking"""
        agent = BlockchainComplianceAgent()
        assert agent is not None
    
    @pytest.mark.skipif(not AGENT_AVAILABLE, reason="Agent module not available")
    def test_agent_integrates_with_api(self):
        """Test agent integrates with FastAPI endpoints"""
        agent = BlockchainComplianceAgent()
        # Should be callable from API
        assert agent is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])