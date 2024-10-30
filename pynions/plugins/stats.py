import time
from .base import Plugin


class StatsPlugin(Plugin):
    """Plugin for tracking and displaying request statistics"""

    def __init__(self, config=None):
        super().__init__(config)
        self.start_time = None
        self.stats = {}

    def initialize(self):
        """Initialize plugin - required by base class"""
        self.start_time = None
        self.stats = {}
        return self

    def cleanup(self):
        """Cleanup plugin resources - required by base class"""
        self.stats = {}
        return self

    def start_tracking(self):
        """Start timing the request"""
        self.start_time = time.time()

    def collect_stats(self, response):
        """Collect stats from response"""
        if not self.start_time:
            return

        duration = round(time.time() - self.start_time, 2)

        self.stats = {
            "duration": duration,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "model": response.model,
        }

    def display_stats(self):
        """Display collected stats"""
        if not self.stats:
            return

        print(f"\n📈 Request Stats:")
        print(f"⏱️  Duration: {self.stats['duration']}s")
        print(
            f"🔤 Tokens Used: {self.stats['total_tokens']} "
            f"({self.stats['input_tokens']} input, "
            f"{self.stats['output_tokens']} output)"
        )
        if self.config.get("show_model", True):
            print(f"🤖 Model: {self.stats['model']}")

    def get_stats(self):
        """Return collected stats"""
        return self.stats.copy()
