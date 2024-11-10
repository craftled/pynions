import pytest
import os
from pynions.plugins.serper import SerperWebSearch


@pytest.fixture
def serper_config():
    """Common Serper configuration for tests"""
    return {"max_results": 10, "api_key": os.getenv("SERPER_API_KEY")}


@pytest.fixture
async def serper_client(serper_config):
    """Initialized Serper client"""
    return SerperWebSearch(serper_config)
