from pynions import Flow, State


class SocialMonitorFlow(Flow):
    """Monitor social media mentions and sentiment"""

    async def run(self):
        async with self.step("fetch_mentions"):
            mentions = await self.fetch_social_mentions()

        async with self.step("analyze_sentiment"):
            sentiment = await self.analyze_sentiment(mentions)

        return {"mentions": mentions, "sentiment": sentiment}
