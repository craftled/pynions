import pytest
from pynions.plugins.serper import SerperWebSearch


@pytest.mark.asyncio
async def test_serper_search():
    """Test basic search functionality"""
    searcher = SerperWebSearch({"max_results": 10})
    result = await searcher.execute({"query": "test query"})

    # Detailed assertions
    assert result is not None
    assert "organic" in result
    assert len(result["organic"]) > 0
    assert isinstance(result["organic"], list)

    # Check first result structure
    first_result = result["organic"][0]
    assert "title" in first_result
    assert "link" in first_result
    assert "snippet" in first_result


@pytest.mark.asyncio
async def test_search_with_invalid_query():
    """Test search with invalid input"""
    searcher = SerperWebSearch({"max_results": 10})

    with pytest.raises(ValueError):
        await searcher.execute({"query": ""})  # Empty query should raise error


@pytest.mark.asyncio
async def test_search_with_custom_params():
    """Test search with custom parameters"""
    searcher = SerperWebSearch(
        {"max_results": 5, "country": "us", "language": "en"}  # Custom limit
    )

    result = await searcher.execute(
        {"query": "test query", "type": "news"}  # Test different search type
    )

    assert len(result["organic"]) <= 5
    assert "country" in result["searchParameters"]
    assert result["searchParameters"]["country"] == "us"


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for invalid API responses"""
    searcher = SerperWebSearch(
        {"api_key": "invalid_key"}  # This should trigger an API error
    )

    with pytest.raises(Exception):  # Replace with your specific error type
        await searcher.execute({"query": "test query"})
