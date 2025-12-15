"""
Tests for configuration module
"""

import pytest
from src.config import ANTHROPIC_MODEL, PROJECT_ROOT, DATA_PATH

def test_config_loaded():
    """Test that configuration is loaded correctly"""
    assert ANTHROPIC_MODEL == "claude-sonnet-4-5-20250929"
    assert PROJECT_ROOT is not None
    assert DATA_PATH is not None

def test_paths_exist():
    """Test that required paths exist"""
    assert PROJECT_ROOT.exists()
    assert DATA_PATH.exists()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
