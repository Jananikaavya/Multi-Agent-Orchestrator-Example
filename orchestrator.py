# orchestrator.py
import asyncio

class MultiAgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.workflows = {}

    def register_agent(self, name: str, agent):
        self.agents[name] = agent
        print(f"✅ Initialized {name} agent")

    def create_workflow(self, name: str):
        workflow_id = name.replace(" ", "_").lower()
        self.workflows[workflow_id] = []
        print(f"📋 Created workflow: {name}")
        return workflow_id

    def add_task(self, workflow_id: str, agent_name: str, method_name: str, args: dict):
        self.workflows[workflow_id].append({
            "agent": agent_name,
            "method": method_name,
            "args": args
        })

    async def execute_workflow(self, workflow_id: str):
        results = []
        tasks = self.workflows.get(workflow_id, [])
        print("🔄 Executing workflow...")
        for t in tasks:
            agent = self.agents[t["agent"]]
            method = getattr(agent, t["method"])
            output = await method(**t["args"])
            results.append(output)
        print("✅ Completed! Generated", len(results), "outputs")
        return results
