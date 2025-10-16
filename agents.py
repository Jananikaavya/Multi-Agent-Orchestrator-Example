"""
Multiple specialized agents using Alith framework
"""

from alith import Agent
from typing import Dict, Any, List
import asyncio


class ResearcherAgent:
    """Agent specialized in research and information gathering"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a professional researcher. Your role is to:
            - Gather and analyze information on given topics
            - Provide comprehensive, well-structured research summaries
            - Cite sources and provide context
            - Identify key points and trends
            - Be thorough and objective in your analysis"""
        )
    
    async def research(self, topic: str) -> str:
        """Conduct research on a given topic"""
        prompt = f"Please research and provide a comprehensive analysis on: {topic}"
        return self.agent.prompt(prompt)


class WriterAgent:
    """Agent specialized in content creation and writing"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a professional writer and content creator. Your role is to:
            - Create engaging, well-structured content
            - Adapt writing style to different audiences and purposes
            - Ensure clarity, coherence, and flow
            - Use appropriate tone and voice
            - Generate creative and original content"""
        )
    
    async def write_content(self, topic: str, content_type: str = "article") -> str:
        """Create written content on a given topic"""
        prompt = f"Please write a {content_type} about: {topic}. Make it engaging and well-structured."
        return self.agent.prompt(prompt)


class AnalyzerAgent:
    """Agent specialized in data analysis and insights"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a data analyst and insight specialist. Your role is to:
            - Analyze data and information systematically
            - Identify patterns, trends, and correlations
            - Provide actionable insights and recommendations
            - Create clear visualizations and summaries
            - Support decision-making with data-driven conclusions"""
        )
    
    async def analyze(self, data: str, analysis_type: str = "general") -> str:
        """Analyze provided data and extract insights"""
        prompt = f"Please perform a {analysis_type} analysis on the following data: {data}"
        return self.agent.prompt(prompt)


class TranslatorAgent:
    """Agent specialized in translation and language services"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a professional translator and language specialist. Your role is to:
            - Provide accurate translations between languages
            - Maintain context and meaning during translation
            - Adapt content culturally when necessary
            - Ensure proper grammar and syntax
            - Support multiple languages and dialects"""
        )
    
    async def translate(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        prompt = f"Please translate the following text to {target_language}: {text}"
        return self.agent.prompt(prompt)


class SummarizerAgent:
    """Agent specialized in summarization and condensation"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a summarization specialist. Your role is to:
            - Create concise, accurate summaries of long texts
            - Preserve key information and main points
            - Adapt summary length to requirements
            - Maintain original meaning and context
            - Structure summaries for easy comprehension"""
        )
    
    async def summarize(self, text: str, max_length: str = "brief") -> str:
        """Summarize provided text"""
        prompt = f"Please provide a {max_length} summary of the following text: {text}"
        return self.agent.prompt(prompt)


class CodeReviewerAgent:
    """Agent specialized in code review and technical analysis"""
    
    def __init__(self):
        self.agent = Agent(
            model="gpt-4",
            preamble="""You are a senior software engineer and code reviewer. Your role is to:
            - Review code for bugs, security issues, and best practices
            - Suggest improvements and optimizations
            - Ensure code follows standards and conventions
            - Provide constructive feedback and recommendations
            - Focus on maintainability, performance, and readability"""
        )
    
    async def review_code(self, code: str, language: str = "python") -> str:
        """Review code and provide feedback"""
        prompt = f"Please review the following {language} code and provide feedback:\n\n{code}"
        return self.agent.prompt(prompt)


# Agent registry for easy access
AGENT_REGISTRY = {
    "researcher": ResearcherAgent,
    "writer": WriterAgent,
    "analyzer": AnalyzerAgent,
    "translator": TranslatorAgent,
    "summarizer": SummarizerAgent,
    "code_reviewer": CodeReviewerAgent
}


async def test_all_agents():
    """Test all agents to ensure they work properly"""
    print("🤖 Testing all agents...")
    
    # Test Researcher Agent
    print("\n📚 Testing Researcher Agent...")
    researcher = ResearcherAgent()
    research_result = await researcher.research("Artificial Intelligence trends in 2024")
    print(f"Research result: {research_result[:200]}...")
    
    # Test Writer Agent
    print("\n✍️ Testing Writer Agent...")
    writer = WriterAgent()
    article = await writer.write_content("Benefits of renewable energy", "article")
    print(f"Article: {article[:200]}...")
    
    # Test Analyzer Agent
    print("\n📊 Testing Analyzer Agent...")
    analyzer = AnalyzerAgent()
    analysis = await analyzer.analyze("Sales increased by 25% this quarter compared to last quarter", "trend")
    print(f"Analysis: {analysis[:200]}...")
    
    # Test Translator Agent
    print("\n🌐 Testing Translator Agent...")
    translator = TranslatorAgent()
    translation = await translator.translate("Hello, how are you today?", "Spanish")
    print(f"Translation: {translation}")
    
    # Test Summarizer Agent
    print("\n📝 Testing Summarizer Agent...")
    summarizer = SummarizerAgent()
    summary = await summarizer.summarize("Artificial intelligence is transforming various industries...", "brief")
    print(f"Summary: {summary[:200]}...")
    
    # Test Code Reviewer Agent
    print("\n💻 Testing Code Reviewer Agent...")
    code_reviewer = CodeReviewerAgent()
    review = await code_reviewer.review_code("def add(a, b):\n    return a + b", "python")
    print(f"Code review: {review[:200]}...")
    
    print("\n✅ All agents tested successfully!")


if __name__ == "__main__":
    asyncio.run(test_all_agents())
