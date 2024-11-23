"""Tests for the config module."""

import os
import json
from pathlib import Path
import pytest
from pynions.core.config import Config

@pytest.fixture(autouse=True)
def clean_env():
    """Clear environment variables before each test."""
    # Save original environment
    original_env = dict(os.environ)
    
    # Clear relevant variables
    for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        if key in os.environ:
            del os.environ[key]
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def temp_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=test-key\nANTHROPIC_API_KEY=test-key-2")
    return env_file

@pytest.fixture
def temp_config_file(tmp_path):
    config_file = tmp_path / "pynions.json"
    config = {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    config_file.write_text(json.dumps(config))
    return config_file

def test_config_singleton():
    """Test that Config is a singleton."""
    config1 = Config()
    config2 = Config()
    assert config1 is config2

def test_config_load_env(temp_env_file):
    """Test loading environment variables."""
    config = Config()
    config.load_env(temp_env_file)
    assert os.getenv("OPENAI_API_KEY") == "test-key"
    assert os.getenv("ANTHROPIC_API_KEY") == "test-key-2"

def test_config_load_json(temp_config_file):
    """Test loading JSON configuration."""
    config = Config()
    config.load_json(temp_config_file)
    assert config.get("model") == "gpt-4o-mini"
    assert config.get("temperature") == 0.7
    assert config.get("max_tokens") == 1000

def test_config_get_default():
    """Test getting config with default value."""
    config = Config()
    assert config.get("non_existent", "default") == "default"

def test_config_set():
    """Test setting config values."""
    config = Config()
    config.set("test_key", "test_value")
    assert config.get("test_key") == "test_value"

def test_config_load_default_paths(temp_env_file, temp_config_file):
    """Test loading from default paths."""
    config = Config()
    
    # Test with custom paths
    config.load(env_path=temp_env_file, config_path=temp_config_file)
    assert os.getenv("OPENAI_API_KEY") == "test-key"
    assert config.get("model") == "gpt-4o-mini"

    # Test with non-existent paths (should not raise errors)
    config.load(env_path=Path("/non/existent/.env"), 
                config_path=Path("/non/existent/pynions.json"))
    
def test_config_clear():
    """Test clearing configuration."""
    config = Config()
    config.set("test_key", "test_value")
    config.clear()
    assert config.get("test_key") is None
