import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Workflow
from pynions.workers.perplexity_definition_worker import PerplexityDefinitionWorker
from pynions.workers.perplexity_methodology_worker import PerplexityMethodologyWorker
from pynions.workers.perplexity_types_worker import PerplexityTypesWorker
from pynions.workers.perplexity_benefits_worker import PerplexityBenefitsWorker
from pynions.workers.perplexity_challenges_worker import PerplexityChallengesWorker
from pynions.workers.perplexity_best_practices_worker import (
    PerplexityBestPracticesWorker,
)
from pynions.workers.perplexity_trends_worker import PerplexityTrendsWorker
from pynions.workers.perplexity_qa_worker import PerplexityQAWorker
from pynions.workers.perplexity_article_writer_worker import (
    PerplexityArticleWriterWorker,
)


class WhatIsWorkflow(Workflow):
    """Workflow for generating comprehensive 'What is [X]?' articles using specialized Perplexity workers"""

    def __init__(self):
        # Initialize all workers
        self.definition_worker = PerplexityDefinitionWorker()
        self.methodology_worker = PerplexityMethodologyWorker()
        self.types_worker = PerplexityTypesWorker()
        self.benefits_worker = PerplexityBenefitsWorker()
        self.challenges_worker = PerplexityChallengesWorker()
        self.best_practices_worker = PerplexityBestPracticesWorker()
        self.trends_worker = PerplexityTrendsWorker()
        self.qa_worker = PerplexityQAWorker()
        self.article_writer = PerplexityArticleWriterWorker()

    def save_results(self, data: Dict, topic: str) -> str:
        """Save the complete article data to a JSON file"""
        # Create articles directory if it doesn't exist
        os.makedirs("data/articles", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/articles/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute the complete workflow to generate a 'What is [X]?' article"""
        topic = input_data["topic"]
        audience = input_data.get("audience", "general readers")
        print(f"\n🔍 Generating comprehensive article about: {topic}")
        print(f"📌 Target audience: {audience}")
        print("⏳ This process may take 15-20 minutes...")

        try:
            # 1. Research Phase
            print("\n📚 Starting Research Phase...")

            # Get definition and origin
            print("\n1️⃣ Researching definition and origin...")
            definition_data = await self.definition_worker.execute({"topic": topic})

            # Get methodology and processes
            print("\n2️⃣ Researching how it works...")
            methodology_data = await self.methodology_worker.execute({"topic": topic})

            # Get types and categories
            print("\n3️⃣ Researching types and categories...")
            types_data = await self.types_worker.execute({"topic": topic})

            # Get benefits and advantages
            print("\n4️⃣ Researching benefits and advantages...")
            benefits_data = await self.benefits_worker.execute({"topic": topic})

            # Get challenges and limitations
            print("\n5️⃣ Researching challenges and limitations...")
            challenges_data = await self.challenges_worker.execute({"topic": topic})

            # Get best practices
            print("\n6️⃣ Researching best practices...")
            best_practices_data = await self.best_practices_worker.execute(
                {"topic": topic}
            )

            # Get future trends
            print("\n7️⃣ Researching future trends...")
            trends_data = await self.trends_worker.execute({"topic": topic})

            # Get Q&A content
            print("\n8️⃣ Generating Q&A content...")
            qa_data = await self.qa_worker.execute({"topic": topic})

            # 2. Compilation Phase
            print("\n📝 Compiling research results...")

            article_data = {
                "topic": topic,
                "audience": audience,
                "timestamp": datetime.now().isoformat(),
                "sections": {
                    "definition": definition_data,
                    "methodology": methodology_data,
                    "types": types_data,
                    "benefits": benefits_data,
                    "challenges": challenges_data,
                    "best_practices": best_practices_data,
                    "trends": trends_data,
                    "qa": qa_data,
                },
                "metadata": {
                    "total_sources": len(
                        set(
                            citation
                            for section_data in [
                                definition_data,
                                methodology_data,
                                types_data,
                                benefits_data,
                                challenges_data,
                                best_practices_data,
                                trends_data,
                                qa_data,
                            ]
                            for citation in section_data.get("citations", [])
                        )
                    ),
                    "generated_at": datetime.now().isoformat(),
                },
            }

            # Save research data
            research_file = self.save_results(article_data, topic)
            print(f"\n💾 Research data saved to: {research_file}")

            # 3. Writing Phase
            print("\n✍️ Starting Writing Phase...")
            article_result = await self.article_writer.execute(
                {"research_data": article_data}
            )

            if article_result:
                print(f"\n🎉 Article successfully generated!")
                print(f"📄 Markdown file: {article_result['file_path']}")
                print(
                    f"📊 Total sources used: {article_result['metadata']['total_citations']}"
                )
                return {"research_data": article_data, "article": article_result}
            else:
                print("\n❌ Failed to generate article")
                return {"research_data": article_data}

        except Exception as e:
            print(f"\n❌ Error during workflow execution: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        workflow = WhatIsWorkflow()
        result = await workflow.execute(
            {"topic": "growth marketing", "audience": "marketing professionals"}
        )

    asyncio.run(test())
