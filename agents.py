# agents.py
import os
from groq import Groq
import asyncio

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        print(f"✅ Using model: {self.model}")
        print(f"✅ Initialized {self.name} agent")

    async def run(self, prompt):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._generate, prompt)

    def _generate(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are a {self.name} AI assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

class ResearcherAgent(BaseAgent):
    pass

class WriterAgent(BaseAgent):
    pass

class AnalyzerAgent(BaseAgent):
    pass

class TranslatorAgent(BaseAgent):
    pass

class SummarizerAgent(BaseAgent):
    pass

class CodeReviewerAgent(BaseAgent):
    pass
