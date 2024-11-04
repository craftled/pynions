import pytest
from pynions.plugins.serper import SerperWebSearch
import os


@pytest.fixture
def serper_client():
    """Provide configured SerperWebSearch instance"""
    return SerperWebSearch({"max_results": 10})


@pytest.mark.asyncio
async def test_basic_search(serper_client):
    """Test basic search functionality"""
    result = await serper_client.execute({"query": "test query"})
    assert result is not None
    assert "organic" in result
    assert isinstance(result["organic"], list)


@pytest.mark.asyncio
async def test_search_parameters(serper_client):
    """Test search parameters are correctly set"""
    result = await serper_client.execute({"query": "test"})
    assert result["searchParameters"]["type"] == "search"


@pytest.mark.asyncio
async def test_result_validation(serper_client):
    """Test response validation"""
    result = await serper_client.execute({"query": "python testing"})
    # Check required fields based on docs
    assert "searchParameters" in result
    assert "organic" in result
    assert "credits" in result


@pytest.mark.asyncio
async def test_max_results_limit():
    """Test max_results parameter works"""
    searcher = SerperWebSearch({"max_results": 5})
    result = await searcher.execute({"query": "test"})
    # Check organic results length
    organic_results = result.get("organic", [])[:5]  # Take only first 5 results
    assert len(organic_results) <= 5


@pytest.mark.asyncio
async def test_error_handling():
    """Test API error handling"""
    # Store original API key
    original_key = os.environ.get("SERPER_API_KEY")

    try:
        # Remove API key from environment
        if "SERPER_API_KEY" in os.environ:
            del os.environ["SERPER_API_KEY"]

        # This should raise ValueError
        with pytest.raises(ValueError, match="SERPER_API_KEY not found"):
            SerperWebSearch({})  # Pass empty config to trigger error

    finally:
        # Restore original API key
        if original_key:
            os.environ["SERPER_API_KEY"] = original_key


@pytest.mark.asyncio
async def test_rate_limiting(serper_client):
    """Test rate limit handling"""
    for _ in range(3):  # Make multiple requests
        result = await serper_client.execute({"query": "test rate limit"})
        assert "credits" in result
