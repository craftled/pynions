import time
from typing import Dict, Any, Optional
from pynions.core import Plugin


class StatsPlugin(Plugin):
    """Plugin for tracking and displaying request statistics"""

    def __init__(self, plugin_config: Optional[Dict[str, Any]] = None):
        super().__init__(plugin_config)
        self.start_time = None
        self.stats = {}

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute stats collection"""
        response = input_data.get("response")
        if not response:
            return {"error": "No response data provided"}

        self.collect_stats(response)
        if self.config.get("auto_display", True):
            self.display_stats()

        return self.get_stats()

    def start_tracking(self) -> None:
        """Start timing the request"""
        self.start_time = time.time()

    def collect_stats(self, response: Any) -> None:
        """Collect stats from response"""
        if not self.start_time:
            return

        duration = round(time.time() - self.start_time, 2)

        self.stats = {
            "duration": duration,
            "input_tokens": getattr(response.usage, "prompt_tokens", 0),
            "output_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
            "model": getattr(response, "model", "unknown"),
        }

    def display_stats(self) -> None:
        """Display collected stats"""
        if not self.stats:
            return

        print("\n📈 Request Stats:")
        print(f"⏱️  Duration: {self.stats['duration']}s")
        print(
            f"🔤 Tokens Used: {self.stats['total_tokens']} "
            f"({self.stats['input_tokens']} input, "
            f"{self.stats['output_tokens']} output)"
        )
        if self.config.get("show_model", True):
            print(f"🤖 Model: {self.stats['model']}")

    def get_stats(self) -> Dict[str, Any]:
        """Return collected stats"""
        return self.stats.copy()


async def test_stats():
    """Test the Stats plugin"""
    try:
        # Create mock response
        class MockUsage:
            prompt_tokens = 100
            completion_tokens = 50
            total_tokens = 150

        class MockResponse:
            usage = MockUsage()
            model = "gpt-4"

        # Initialize plugin
        stats = StatsPlugin({"show_model": True, "auto_display": True})

        # Start tracking
        stats.start_tracking()

        # Simulate some work
        await asyncio.sleep(1)

        # Execute with mock response
        result = await stats.execute({"response": MockResponse()})

        print("\n✅ Successfully collected stats!")
        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_stats())
