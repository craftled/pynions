import pytest
import asyncio
from pynions.plugins.perplexity import PerplexityAPI


@pytest.mark.asyncio
async def test_perplexity_direct_question():
    """Test direct question answering"""
    perplexity = PerplexityAPI()

    response = await perplexity.execute(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What are the key features of Python programming language?",
                }
            ]
        }
    )

    assert response is not None
    assert "choices" in response
    assert len(response["choices"]) > 0
    assert "citations" in response


@pytest.mark.asyncio
async def test_perplexity_research():
    """Test web research capabilities"""
    perplexity = PerplexityAPI()

    response = await perplexity.execute(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a technology researcher. Provide factual, well-cited information.",
                },
                {
                    "role": "user",
                    "content": "What are the latest developments in AI regulation in the EU?",
                },
            ]
        }
    )

    assert response is not None
    assert "choices" in response
    assert "citations" in response
    # Should have citations since it's a research question
    assert len(response.get("citations", [])) > 0


@pytest.mark.asyncio
async def test_perplexity_structured_output():
    """Test getting structured data output"""
    perplexity = PerplexityAPI()

    response = await perplexity.execute(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data extractor. Return information in JSON format only.",
                },
                {
                    "role": "user",
                    "content": "List the top 3 cloud providers and their key services in JSON format",
                },
            ]
        }
    )

    assert response is not None
    assert "choices" in response
    content = response["choices"][0]["message"]["content"]
    assert "{" in content and "}" in content  # Should contain JSON


@pytest.mark.asyncio
async def test_perplexity_custom_config():
    """Test with custom configuration"""
    perplexity = PerplexityAPI(
        {
            "temperature": 0,  # More deterministic
            "max_tokens": 100,  # Shorter response
        }
    )

    response = await perplexity.execute(
        {"messages": [{"role": "user", "content": "What is 2+2? Answer in one word."}]}
    )

    assert response is not None
    assert "choices" in response
    # Response should be concise due to max_tokens
    assert len(response["choices"][0]["message"]["content"]) < 10


if __name__ == "__main__":
    asyncio.run(test_perplexity_direct_question())
    asyncio.run(test_perplexity_research())
    asyncio.run(test_perplexity_structured_output())
    asyncio.run(test_perplexity_custom_config())
