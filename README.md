# Multi-Agent Orchestrator Workshop

A AI-powered multi-agent system using Alith framework with 6 specialized agents that can work together asynchronously.

## What This System Does

- **6 Specialized AI Agents**: Researcher, Writer, Analyzer, Translator, Summarizer, Code Reviewer
- **Multi-Agent Orchestrator**: Coordinates agents in sequential or parallel workflows
- **Real AI Responses**: Uses OpenAI GPT-4 for all agent interactions
- **Async Execution**: Handles multiple agents working together efficiently

## Prerequisites

- Python 3.8+
- OpenAI API Key

## Step-by-Step Setup

### 1. Clone/Download the Project
```bash
git clone  https://github.com/0xLazAI/Multi-Agent-Orchestrator-Example.git
cd Multi-Agent-Orchestrator-Example
# Extract or clone the multiagent folder
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up OpenAI API Key

**On macOS/Linux:**
```bash
export OPENAI_API_KEY=your_api_key_here
```

**On Windows:**
```bash
set OPENAI_API_KEY=your_api_key_here
```

## Running the System

### Basic Execution
```bash
python run.py
```

This will:
1. Initialize all 6 AI agents
2. Create a research and write workflow
3. Execute the workflow with real AI responses
4. Display the results

### Expected Output
```
🚀 Multi-Agent Orchestrator
========================================
✅ Initialized researcher agent
✅ Initialized writer agent
✅ Initialized analyzer agent
✅ Initialized translator agent
✅ Initialized summarizer agent
✅ Initialized code_reviewer agent
📋 Created workflow: Research and Write Pipeline
🔄 Executing workflow...
✅ Completed! Generated 2 outputs

📊 Result: [Real AI research output]
📊 Result: [Real AI article output]
```

## Available Agents

| Agent | Purpose | Method |
|-------|---------|---------|
| **Researcher** | Research and analysis | `research(topic)` |
| **Writer** | Content creation | `write_content(topic, type)` |
| **Analyzer** | Data analysis | `analyze(data, type)` |
| **Translator** | Language translation | `translate(text, language)` |
| **Summarizer** | Text summarization | `summarize(text, length)` |
| **Code Reviewer** | Code review | `review_code(code, language)` |

## Creating Custom Workflows

```python
import asyncio
from orchestrator import MultiAgentOrchestrator, WorkflowType

async def custom_workflow():
    # Initialize
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize_agents()
    
    # Create workflow
    workflow_id = orchestrator.create_workflow(
        name='Custom Pipeline',
        workflow_type=WorkflowType.SEQUENTIAL
    )
    
    # Add tasks
    task1 = orchestrator.add_task_to_workflow(
        workflow_id, 'researcher', 'research', {'topic': 'Your Topic'}
    )
    
    task2 = orchestrator.add_task_to_workflow(
        workflow_id, 'writer', 'write_content', 
        {'topic': 'Your Topic', 'content_type': 'article'},
        dependencies=[task1]
    )
    
    # Execute
    results = await orchestrator.execute_workflow(workflow_id)
    return results

# Run custom workflow
asyncio.run(custom_workflow())
```

## Workflow Types

- **Sequential**: Tasks run one after another
- **Parallel**: Tasks run simultaneously when dependencies allow
- **Custom**: User-defined with specific dependencies

## Troubleshooting

### API Key Issues
```bash
echo $OPENAI_API_KEY  # Check if key is set
```

### Virtual Environment Issues
```bash
deactivate  # Exit virtual environment
source venv/bin/activate  # Re-enter (macOS/Linux)
```

### Dependencies Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Workshop Exercises

1. **Run the basic system**: `python run.py`
2. **Modify the topic**: Change "AI in Healthcare" to your topic
3. **Add more agents**: Include translator or analyzer in the workflow
4. **Create parallel workflow**: Use WorkflowType.PARALLEL
5. **Custom workflow**: Build your own agent sequence

## Files Structure

```
multiagent/
├── agents.py          # All 6 AI agents
├── orchestrator.py    # Multi-agent orchestrator
├── run.py            # Basic execution example
├── requirements.txt   # Dependencies
└── venv/             # Virtual environment
```

## Next Steps

- Modify agent prompts for your use case
- Add new specialized agents
- Create complex multi-step workflows
- Integrate with your applications
- Scale to production workloads

