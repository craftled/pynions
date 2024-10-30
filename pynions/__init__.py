"""
Pynions - A lean Python framework for marketers who code
Built for automating marketing tasks without the bloat.
"""

from pynions.core import Plugin, Workflow, WorkflowStep, Config, DataStore

# Import built-in plugins
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.litellm import LiteLLMPlugin
from pynions.plugins.playwright import PlaywrightPlugin
from pynions.plugins.jina import JinaPlugin
from pynions.plugins.stats import StatsPlugin

__version__ = "0.1.0"

__all__ = [
    # Core components
    "Plugin",
    "Workflow",
    "WorkflowStep",
    "Config",
    "DataStore",
    # Built-in plugins
    "SerperWebSearch",
    "LiteLLMPlugin",
    "PlaywrightPlugin",
    "JinaPlugin",
    "StatsPlugin",
]
