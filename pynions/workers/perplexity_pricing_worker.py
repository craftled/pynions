import asyncio
import json
import traceback
import time
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI

# ANSI Color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"
BOLD = "\033[1m"


class Spinner:
    """Simple spinner animation for terminal feedback"""

    def __init__(self, message=""):
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.message = message
        self.current = 0
        self.active = False

    def spin(self):
        """Print next spinner frame"""
        if self.active:
            sys.stdout.write(
                "\r" + self.spinner_chars[self.current] + " " + self.message
            )
            sys.stdout.flush()
            self.current = (self.current + 1) % len(self.spinner_chars)

    def start(self, message=""):
        """Start spinner animation"""
        if message:
            self.message = message
        self.active = True
        self.spin()

    def stop(self):
        """Stop spinner animation"""
        self.active = False
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()


class PerplexityPricingWorker(Worker):
    """Worker for extracting pricing data from a website using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,
                "max_tokens": 2000,
                "return_related_questions": False,
            }
        )
        self.spinner = Spinner()

    def validate_pricing_data(self, data: Dict) -> bool:
        """Validate the structure and content of pricing data"""
        try:
            print(f"{CYAN}🔍 Validating pricing data structure and sources...{RESET}")

            # Check required top-level keys
            required_keys = ["plans", "pricing", "currency", "sources"]
            if not all(key in data for key in required_keys):
                print(
                    f"{RED}❌ Missing required keys:{RESET}",
                    [k for k in required_keys if k not in data],
                )
                return False

            # Validate plans array
            if not isinstance(data["plans"], list) or not data["plans"]:
                print(f"{RED}❌ Invalid or empty plans array{RESET}")
                return False

            # Validate pricing structure
            pricing = data["pricing"]
            if not isinstance(pricing, dict):
                print(f"{RED}❌ Invalid pricing structure{RESET}")
                return False

            # Check each plan has required structure and source verification
            for plan_name in data["plans"]:
                if plan_name not in pricing:
                    print(f"{RED}❌ Missing pricing data for plan: {plan_name}{RESET}")
                    return False

                plan = pricing[plan_name]
                if not isinstance(plan, dict):
                    print(f"{RED}❌ Invalid plan structure for: {plan_name}{RESET}")
                    return False

                # Validate features have source information
                if "features" in plan:
                    for feature in plan["features"]:
                        if not all(
                            key in feature
                            for key in ["name", "source_url", "source_quote"]
                        ):
                            print(
                                f"{RED}❌ Missing source verification for feature in plan: {plan_name}{RESET}"
                            )
                            return False

                # Validate limits have source information
                if "limits" in plan:
                    for limit_name, limit_data in plan["limits"].items():
                        if not all(
                            key in limit_data
                            for key in ["value", "source_url", "source_quote"]
                        ):
                            print(
                                f"{RED}❌ Missing source verification for limit in plan: {plan_name}{RESET}"
                            )
                            return False

            # Validate sources structure with enhanced verification
            sources = data["sources"]
            if not isinstance(sources, dict):
                print(f"{RED}❌ Invalid sources structure{RESET}")
                return False

            # Check primary source
            if "primary" not in sources:
                print(f"{RED}❌ Missing primary source{RESET}")
                return False

            primary = sources["primary"]
            if not all(
                key in primary for key in ["url", "last_checked", "content_hash"]
            ):
                print(
                    f"{RED}❌ Invalid primary source structure - missing verification data{RESET}"
                )
                return False

            # Verify all sources are official
            if "additional" in sources:
                if not isinstance(sources["additional"], list):
                    print(f"{RED}❌ Invalid additional sources structure{RESET}")
                    return False

                for idx, source in enumerate(sources["additional"]):
                    if not all(
                        key in source
                        for key in [
                            "url",
                            "type",
                            "section",
                            "last_checked",
                            "content_hash",
                        ]
                    ):
                        print(
                            f"{RED}❌ Invalid structure for additional source {idx + 1}{RESET}"
                        )
                        return False

                    if source["type"] != "official":
                        print(
                            f"{RED}❌ Non-official source detected: {source['url']}{RESET}"
                        )
                        return False

            print(f"{GREEN}✅ Pricing data structure and sources verified{RESET}")
            print(f"{BLUE}🔗 Primary source: {sources['primary']['url']}{RESET}")
            if sources.get("additional"):
                print(
                    f"{BLUE}📚 Additional official sources: {len(sources['additional'])}{RESET}"
                )

            return True
        except Exception as e:
            print(f"{RED}❌ Validation error: {str(e)}{RESET}")
            return False

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract and structure pricing data from a domain using Perplexity AI"""
        domain = input_data["domain"]
        start_time = time.time()
        print(f"\n{BLUE}🔍 Analyzing pricing for {BOLD}{domain}{RESET}")
        print(f"{YELLOW}⏳ This may take up to 3 minutes...{RESET}")

        try:
            # Use Perplexity to research and analyze pricing
            print("\n📊 Process started:")
            print("1. 🤖 Initializing AI model...")

            # Start spinner for the research phase
            self.spinner.start("2. 🔎 Researching pricing information...")

            # Setup the request payload
            messages = [
                {
                    "role": "system",
                    "content": """Extract pricing information from the company's website with strict first-party verification.

Requirements:
1. ONLY use official company sources (help center, docs, pricing pages)
2. For each fact or number, include the exact source URL and relevant quote
3. Cross-reference all information within official documentation
4. Note any conditions or exceptions that apply to limits/features
5. Include full context for any limitations or restrictions
6. Maintain precise wording from source material

Output Format:
{
    "plans": ["plan names"],
    "pricing": {
        "plan_name": {
            "monthly_price": number_or_string,
            "annual_price": number_or_string,
            "features": [
                {
                    "name": "feature name",
                    "description": "exact feature description from source",
                    "source_url": "direct link to feature documentation",
                    "source_quote": "exact quote from documentation"
                }
            ],
            "limits": {
                "limit_name": {
                    "value": "exact limit value",
                    "conditions": ["any conditions that apply"],
                    "source_url": "direct link to limit documentation",
                    "source_quote": "exact quote describing the limit"
                }
            }
        }
    },
    "currency": "USD",
    "sources": {
        "primary": {
            "url": "direct link to official pricing page",
            "last_checked": "YYYY-MM-DD",
            "content_hash": "hash of page content for verification"
        },
        "additional": [
            {
                "url": "link to official documentation page",
                "type": "official",
                "section": "specific section or heading",
                "last_checked": "YYYY-MM-DD",
                "content_hash": "hash of page content"
            }
        ]
    }
}""",
                },
                {
                    "role": "user",
                    "content": f"Research and analyze the current pricing structure for {domain}. ONLY use official company sources (pricing pages, help center, documentation). For each fact, feature, or limit, include the exact source URL and quote. Return the data in the specified JSON format.",
                },
            ]

            # Make the API request with progress updates
            last_update = time.time()
            response = None

            async def update_spinner():
                while not response:
                    current_time = time.time()
                    if current_time - last_update > 1:  # Update every second
                        sys.stdout.write(
                            f"\r{CYAN}🔎 Researching... ({(current_time - start_time):.0f}s elapsed){RESET}"
                        )
                        sys.stdout.flush()
                        await asyncio.sleep(1)

            # Start progress update task
            progress_task = asyncio.create_task(update_spinner())

            # Make the actual API request
            response = await self.perplexity.execute({"messages": messages})

            # Stop spinner
            self.spinner.stop()

            elapsed_time = time.time() - start_time
            print(f"\n{GREEN}✨ Response received in {elapsed_time:.1f} seconds{RESET}")
            print(f"{BLUE}📚 Found {len(response.get('citations', []))} sources{RESET}")

            # Parse and validate response
            if not response.get("choices"):
                raise ValueError("No choices in response")

            content = response["choices"][0]["message"]["content"].strip()
            print(f"\n{CYAN}🔄 Processing response...{RESET}")

            # Clean and parse JSON
            if not content.startswith("{"):
                print(f"{YELLOW}🔧 Cleaning response format...{RESET}")
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    content = content[start:end]

            content = (
                content.replace("'", '"').replace("```json\n", "").replace("\n```", "")
            )
            pricing_data = json.loads(content)

            # Validate the data
            if not self.validate_pricing_data(pricing_data):
                raise ValueError("Invalid pricing data structure")

            print(f"\n{GREEN}✅ Successfully extracted pricing information:{RESET}")
            print(f"{BLUE}📋 Found {len(pricing_data['plans'])} pricing plans{RESET}")
            print(f"{BLUE}💰 Currency: {pricing_data['currency']}{RESET}")

            result = {
                "domain": domain,
                "sources": response.get("citations", []),
                "pricing": pricing_data,
                "metadata": {
                    "timestamp": response.get("created"),
                    "model": response.get("model"),
                    "token_usage": response.get("usage", {}),
                },
            }

            print(
                f"\n{GREEN}🎉 Total processing time: {time.time() - start_time:.1f} seconds{RESET}"
            )
            return result

        except json.JSONDecodeError as e:
            self.spinner.stop()
            print(f"\n{RED}❌ JSON parsing error:{RESET}")
            print(f"{RED}Error message: {str(e)}{RESET}")
            return None
        except Exception as e:
            self.spinner.stop()
            print(f"\n{RED}❌ Error details:{RESET}")
            print(f"{RED}Error type: {type(e).__name__}{RESET}")
            print(f"{RED}Error message: {str(e)}{RESET}")
            print("Full traceback:")
            traceback.print_exc()
            return None


# Test
if __name__ == "__main__":

    async def test():
        worker = PerplexityPricingWorker()
        result = await worker.execute({"domain": "notion.so"})
        if result:
            print("\n📝 Pricing Data:")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Failed to get pricing data")

    asyncio.run(test())
