import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
from pynions import Worker
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader
from pynions.plugins.litellm_plugin import LiteLLM


class CompanyDataWorker(Worker):
    """Worker for extracting specific data types from company websites"""

    def __init__(self):
        self.serper = SerperWebSearch({"max_results": 5})
        self.jina = JinaAIReader()
        self.llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract specific data from a company website

        Args:
            input_data: dict containing:
                - domain: str - Company domain to analyze
                - data_type: str - Type of data to extract (pricing/features/integrations/about)
        """
        domain = input_data["domain"]
        data_type = input_data["data_type"]

        if data_type not in ["pricing", "features", "integrations", "about"]:
            print(f"❌ Invalid data type: {data_type}")
            return None

        print(f"\n🔍 Verifying {data_type} data for {domain}")

        search_queries = {
            "pricing": f"site:{domain} pricing",
            "features": f"site:{domain} features",
            "integrations": f"site:{domain} integrations",
            "about": f"site:{domain} about",
        }

        try:
            # Search for relevant pages
            print(f"   Searching: {search_queries[data_type]}")
            results = await self.serper.execute({"query": search_queries[data_type]})

            if not results.get("organic"):
                print("   ⚠️ No search results found")
                return None

            # Extract content from each result
            verified_data = []
            total_chars = 0

            for idx, result in enumerate(results["organic"], 1):
                url = result["link"]
                print(f"   Processing {idx}/5: {url}")

                try:
                    content = await self.jina.execute({"url": url})
                    if content and content.get("content"):
                        content_length = len(content["content"])
                        total_chars += content_length
                        print(f"   ✅ Content extracted: {content_length} characters")
                        verified_data.append(
                            {
                                "url": url,
                                "content": content["content"],
                                "title": result.get("title", ""),
                                "snippet": result.get("snippet", ""),
                                "length": content_length,
                            }
                        )
                    else:
                        print("   ⚠️ No content extracted")
                except Exception as e:
                    print(f"   ❌ Error extracting content: {str(e)}")
                    continue

            # Combine all content for LLM analysis
            combined_content = "\n\n".join(
                [source["content"] for source in verified_data]
            )

            # Get LLM prompt based on data type
            prompts = {
                "pricing": """Extract exact pricing information. Include:
                    - Plan names and prices (monthly/annual)
                    - Features and limits for each plan
                    - Currency used""",
                "features": """Extract main product features. Include:
                    - Core features list
                    - Key capabilities
                    - Notable functionalities""",
                "integrations": """Extract integration information. Include:
                    - Available integration categories
                    - Specific integration names
                    - API/webhook capabilities""",
                "about": """Extract company information. Include:
                    - Company background
                    - Key team members
                    - Mission/values
                    - Notable achievements""",
            }

            # Analyze with LLM
            print(f"\n🤖 Analyzing {data_type} content...")
            response = await self.llm.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": f"""You are a precise data extractor. Extract {data_type} information from websites.
                        Instructions:
                        1. Only include information explicitly stated in the content
                        2. Use exact text and values as shown
                        3. Do not make assumptions
                        4. If information is not found, exclude it
                        
                        {prompts[data_type]}
                        
                        IMPORTANT: Respond ONLY with a valid JSON object.""",
                        },
                        {
                            "role": "user",
                            "content": f"Extract {data_type} information from this content:\n\n{combined_content}",
                        },
                    ]
                }
            )

            # Parse LLM response and handle potential errors
            try:
                # Extract JSON from response - handle potential text wrapping
                response_text = response["content"].strip()
                if response_text.startswith("```json"):
                    response_text = response_text.split("```json")[1]
                if response_text.endswith("```"):
                    response_text = response_text.rsplit("```", 1)[0]

                analyzed_data = json.loads(response_text.strip())
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing LLM response: {str(e)}")
                print(f"Raw response: {response['content']}")
                analyzed_data = {"error": "Failed to parse LLM response"}

            # Update response data
            response_data = {
                "domain": domain,
                "data_type": data_type,
                "sources": verified_data,
                "total_chars": total_chars,
                "analyzed_data": analyzed_data,
                "credits_used": results.get("credits", 0),
                "timestamp": datetime.now().isoformat(),
            }

            print(f"\n✅ Analysis complete")
            return response_data

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        worker = CompanyDataWorker()  # Create worker instance
        test_cases = [
            {"domain": "klaviyo.com", "data_type": "pricing"},
            {"domain": "mailchimp.com", "data_type": "features"},
            {"domain": "hubspot.com", "data_type": "integrations"},
            {"domain": "resend.com", "data_type": "about"},
        ]

        for test_case in test_cases:
            print(f"\n📌 Testing {test_case['data_type']} for {test_case['domain']}")
            result = await worker.execute(test_case)

            if result:
                print("\nExtracted Data:")
                print(
                    json.dumps(
                        {
                            "domain": result["domain"],
                            "data_type": result["data_type"],
                            "sources_count": len(result["sources"]),
                            "total_chars": result["total_chars"],
                            "credits_used": result["credits_used"],
                            "timestamp": result["timestamp"],
                        },
                        indent=2,
                    )
                )

                print("\nAnalyzed Data:")
                print(json.dumps(result["analyzed_data"], indent=2))

                print("\nContent Preview:")
                for idx, source in enumerate(result["sources"], 1):
                    print(f"\n{idx}. {source['url']}")
                    print(f"   Title: {source['title']}")
                    print(f"   Content Length: {source['length']} chars")

                if result.get("credits_used"):
                    print(f"\n💰 Credits Used: {result['credits_used']}")

            print("-" * 50)

    asyncio.run(test())
