import os
import asyncio
import requests

# ========== BASE AGENT ==========
class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, *args, **kwargs):
        raise NotImplementedError(f"{self.name} must implement run() method.")


# ========== GROQ CHAT FUNCTION ==========
def groq_chat(prompt):
    """Helper to call Groq API and return text."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        return "[Error] GROQ_API_KEY not found."

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                            headers=headers, json=data).json()
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Error] Groq call failed: {e}"


# ========== AGENTS ==========
class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("researcher")

    async def run(self, topic):
        print(f"🔍 Researcher is researching about: {topic}")
        prompt = f"Provide an in-depth research summary about: {topic}. Include statistics, benefits, and challenges."
        return groq_chat(prompt)


class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__("analyzer")

    async def run(self, content):
        print("🧠 Analyzer is summarizing the research data...")
        prompt = f"Summarize this content into concise, bullet-point key insights:\n\n{content}"
        return groq_chat(prompt)


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("writer")

    async def run(self, summary):
        print("✍️ Writer is creating a detailed article...")
        prompt = f"Write a detailed and engaging article based on this summary:\n\n{summary}\n\nFormat with headings and clear sections."
        return groq_chat(prompt)


class TranslatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("translator")

    async def run(self, text, lang="Tamil"):
        print(f"🌐 Translator translating article to {lang}...")
        prompt = f"Translate the following English text into {lang}:\n\n{text}"
        return groq_chat(prompt)


# ========== ORCHESTRATOR ==========
class Orchestrator:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent
        print(f"✅ Initialized {name} agent")

    async def run_workflow(self, topic):
        print("\n📋 Starting Workflow: Research → Analyze → Write → Translate\n")

        researcher = self.agents["researcher"]
        analyzer = self.agents["analyzer"]
        writer = self.agents["writer"]
        translator = self.agents["translator"]

        # Step 1: Research
        research_data = await researcher.run(topic)
        print("\n📊 Research Output:\n", research_data[:400], "...\n")

        # Step 2: Analyze
        summary = await analyzer.run(research_data)
        print("📑 Summary:\n", summary[:400], "...\n")

        # Step 3: Write
        article = await writer.run(summary)
        print("📰 Article:\n", article[:400], "...\n")

        # Step 4: Translate
        translated = await translator.run(article, "Tamil")
        print("🌍 Translated Version:\n", translated[:400], "...\n")

        print("✅ Workflow Completed Successfully!")
        return {
            "research": research_data,
            "summary": summary,
            "article": article,
            "translated": translated
        }


# ========== MAIN ==========
async def main():
    print("\n🚀 Multi-Agent Orchestrator (Groq Only)\n" + "=" * 50)

    orchestrator = Orchestrator()
    orchestrator.register_agent("researcher", ResearcherAgent())
    orchestrator.register_agent("analyzer", AnalyzerAgent())
    orchestrator.register_agent("writer", WriterAgent())
    orchestrator.register_agent("translator", TranslatorAgent())

    topic = input("\n🔎 Enter a topic to research: ")
    results = await orchestrator.run_workflow(topic)

    print("\n🧾 Final Results Summary:")
    for key, val in results.items():
        print(f"\n🔹 {key.upper()}:\n{val[:500]}...\n")


if __name__ == "__main__":
    asyncio.run(main())
