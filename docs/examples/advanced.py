import os
from datetime import datetime
import litellm
from litellm import completion
import openai
from pynions import StatsPlugin

# Default configuration
DEFAULT_CONFIG = {
    "model": {
        "name": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 500,
    },
    "output": {
        "stream": True,
        "save_results": True,
    },
    "prompt": {"template": "Give me 3 key points about: {topic}. Be concise."},
    "plugins": {
        "stats": {
            "enabled": True,
            "show_model": True,
        }
    },
}


def load_config(custom_config=None):
    """Load and merge configuration"""
    config = DEFAULT_CONFIG.copy()
    if custom_config:
        config.update(custom_config)
    return config


class QuickAI:
    def __init__(self, custom_config=None):
        self.config = load_config(custom_config)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please add your OpenAI API key to .env file")
        os.environ["OPENAI_API_KEY"] = self.api_key

        # Initialize plugins
        self.plugins = {}
        if self.config["plugins"]["stats"]["enabled"]:
            self.plugins["stats"] = StatsPlugin(self.config["plugins"]["stats"])
            self.plugins["stats"].initialize()

    def analyze(self, topic):
        """Analyze a topic using the configured LLM"""
        try:
            messages = [
                {
                    "role": "user",
                    "content": self.config["prompt"]["template"].format(topic=topic),
                }
            ]

            # Start stats tracking if enabled
            stats_plugin = self.plugins.get("stats")
            if stats_plugin:
                stats_plugin.start_tracking()

            if self.config["output"]["stream"]:
                # Get stats from non-streaming request
                response = completion(
                    model=self.config["model"]["name"],
                    messages=messages,
                    temperature=self.config["model"]["temperature"],
                    stream=False,
                )

                if stats_plugin:
                    stats_plugin.collect_stats(response)

                # Stream the response
                print("\n📊 Analysis Results:")
                print("------------------")
                for chunk in completion(
                    model=self.config["model"]["name"],
                    messages=messages,
                    temperature=self.config["model"]["temperature"],
                    stream=True,
                ):
                    if chunk and chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="", flush=True)

                print()  # New line after streaming

                # Display stats if enabled
                if stats_plugin:
                    stats_plugin.display_stats()

                return response.choices[0].message.content
            else:
                # Non-streaming response
                response = completion(
                    model=self.config["model"]["name"],
                    messages=messages,
                    temperature=self.config["model"]["temperature"],
                )

                print("\n📊 Analysis Results:")
                print("------------------")
                print(response.choices[0].message.content)

                if stats_plugin:
                    stats_plugin.collect_stats(response)
                    stats_plugin.display_stats()

                return response.choices[0].message.content

        except openai.OpenAIError as e:
            return f"OpenAI API Error: {str(e)}"
        except Exception as e:
            return f"Unexpected Error: {str(e)}"
        finally:
            # Cleanup plugins
            for plugin in self.plugins.values():
                plugin.cleanup()


def save_result(content, prefix="analysis"):
    """Save content to a file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{prefix}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(content)

    return filename


def main():
    print("\n🤖 Pynions Quick Start Demo")
    print("---------------------------")

    try:
        ai = QuickAI()
        topic = input("\n📝 Enter a topic to analyze: ")

        print("\n🔄 Analyzing...")
        result = ai.analyze(topic)

        # Save result
        if result:
            filename = save_result(result)
            print(f"\n✅ Results saved to: {filename}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Check if OPENAI_API_KEY is set in .env")
        print("2. Verify internet connection")
        print("3. Ensure OpenAI API is accessible")


if __name__ == "__main__":
    main()
