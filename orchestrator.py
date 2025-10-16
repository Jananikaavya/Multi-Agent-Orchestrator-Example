"""
Multi-Agent Orchestrator using Alith
Manages and coordinates multiple agents asynchronously
"""

import asyncio
import uuid
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from agents import AGENT_REGISTRY


class TaskStatus(Enum):
    """Status of a task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowType(Enum):
    """Types of workflows"""
    SEQUENTIAL = "sequential"  # Tasks run one after another
    PARALLEL = "parallel"      # Tasks run simultaneously
    CONDITIONAL = "conditional"  # Tasks run based on conditions
    PIPELINE = "pipeline"      # Data flows through agents sequentially


@dataclass
class Task:
    """Represents a single task in the workflow"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: str = ""
    method: str = ""
    args: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)  # Task IDs this depends on


@dataclass
class Workflow:
    """Represents a complete workflow"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    workflow_type: WorkflowType = WorkflowType.SEQUENTIAL
    tasks: List[Task] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    results: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to work together"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        
    def initialize_agents(self, agent_types: List[str] = None):
        """Initialize agents from the registry"""
        if agent_types is None:
            agent_types = list(AGENT_REGISTRY.keys())
            
        for agent_type in agent_types:
            if agent_type in AGENT_REGISTRY:
                self.agents[agent_type] = AGENT_REGISTRY[agent_type]()
                print(f"✅ Initialized {agent_type} agent")
            else:
                print(f"❌ Unknown agent type: {agent_type}")
    
    def create_workflow(self, name: str, description: str = "", 
                       workflow_type: WorkflowType = WorkflowType.SEQUENTIAL) -> str:
        """Create a new workflow"""
        workflow = Workflow(
            name=name,
            description=description,
            workflow_type=workflow_type
        )
        self.workflows[workflow.id] = workflow
        print(f"📋 Created workflow: {name} (ID: {workflow.id})")
        return workflow.id
    
    def add_task_to_workflow(self, workflow_id: str, agent_type: str, 
                           method: str, args: Dict[str, Any] = None,
                           dependencies: List[str] = None) -> str:
        """Add a task to a workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if args is None:
            args = {}
        if dependencies is None:
            dependencies = []
            
        task = Task(
            agent_type=agent_type,
            method=method,
            args=args,
            dependencies=dependencies
        )
        
        self.workflows[workflow_id].tasks.append(task)
        print(f"➕ Added task {task.id} ({agent_type}.{method}) to workflow {workflow_id}")
        return task.id
    
    async def execute_task(self, task: Task) -> Any:
        """Execute a single task"""
        try:
            task.status = TaskStatus.IN_PROGRESS
            print(f"🔄 Executing task {task.id}: {task.agent_type}.{task.method}")
            
            if task.agent_type not in self.agents:
                raise ValueError(f"Agent {task.agent_type} not initialized")
            
            agent = self.agents[task.agent_type]
            method = getattr(agent, task.method)
            
            # Execute the agent method (all agent methods are async but call sync Alith methods)
            result = await method(**task.args)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            print(f"✅ Task {task.id} completed successfully")
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            print(f"❌ Task {task.id} failed: {e}")
            raise
    
    def get_task_dependencies_met(self, task: Task, completed_tasks: set) -> bool:
        """Check if all dependencies for a task are met"""
        return all(dep_id in completed_tasks for dep_id in task.dependencies)
    
    async def execute_workflow_sequential(self, workflow_id: str) -> Dict[str, Any]:
        """Execute workflow tasks sequentially"""
        workflow = self.workflows[workflow_id]
        workflow.status = TaskStatus.IN_PROGRESS
        results = {}
        completed_tasks = set()
        
        print(f"🚀 Starting sequential execution of workflow: {workflow.name}")
        
        while len(completed_tasks) < len(workflow.tasks):
            executed_this_round = False
            
            for task in workflow.tasks:
                if (task.status == TaskStatus.PENDING and 
                    self.get_task_dependencies_met(task, completed_tasks)):
                    
                    result = await self.execute_task(task)
                    results[task.id] = result
                    completed_tasks.add(task.id)
                    executed_this_round = True
            
            if not executed_this_round:
                # Check for circular dependencies or missing dependencies
                pending_tasks = [t for t in workflow.tasks if t.status == TaskStatus.PENDING]
                if pending_tasks:
                    print(f"⚠️ Warning: Some tasks cannot be executed due to dependency issues")
                    for task in pending_tasks:
                        print(f"   - Task {task.id} dependencies: {task.dependencies}")
                break
        
        workflow.status = TaskStatus.COMPLETED
        workflow.completed_at = datetime.now()
        workflow.results = results
        
        print(f"✅ Workflow {workflow.name} completed!")
        return results
    
    async def execute_workflow_parallel(self, workflow_id: str) -> Dict[str, Any]:
        """Execute workflow tasks in parallel (respecting dependencies)"""
        workflow = self.workflows[workflow_id]
        workflow.status = TaskStatus.IN_PROGRESS
        results = {}
        
        print(f"🚀 Starting parallel execution of workflow: {workflow.name}")
        
        # Group tasks by dependency level
        task_groups = self._group_tasks_by_dependency_level(workflow.tasks)
        
        for level, tasks in task_groups.items():
            print(f"📊 Executing dependency level {level} with {len(tasks)} tasks")
            
            # Execute all tasks in this level in parallel
            task_coroutines = []
            for task in tasks:
                if task.status == TaskStatus.PENDING:
                    task_coroutines.append(self.execute_task(task))
            
            if task_coroutines:
                task_results = await asyncio.gather(*task_coroutines, return_exceptions=True)
                
                # Store results
                for i, task in enumerate(tasks):
                    if task.status == TaskStatus.PENDING:
                        if isinstance(task_results[i], Exception):
                            print(f"❌ Task {task.id} failed: {task_results[i]}")
                        else:
                            results[task.id] = task_results[i]
        
        workflow.status = TaskStatus.COMPLETED
        workflow.completed_at = datetime.now()
        workflow.results = results
        
        print(f"✅ Workflow {workflow.name} completed!")
        return results
    
    def _group_tasks_by_dependency_level(self, tasks: List[Task]) -> Dict[int, List[Task]]:
        """Group tasks by their dependency level"""
        levels = {}
        task_ids = {task.id for task in tasks}
        
        def get_level(task_id: str, visited: set = None) -> int:
            if visited is None:
                visited = set()
            if task_id in visited:
                return 0  # Circular dependency
            
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                return 0
            
            if not task.dependencies:
                return 0
            
            max_dep_level = 0
            for dep_id in task.dependencies:
                if dep_id in task_ids:
                    dep_level = get_level(dep_id, visited | {task_id})
                    max_dep_level = max(max_dep_level, dep_level + 1)
            
            return max_dep_level
        
        for task in tasks:
            level = get_level(task.id)
            if level not in levels:
                levels[level] = []
            levels[level].append(task)
        
        return levels
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow based on its type"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        if workflow.workflow_type == WorkflowType.SEQUENTIAL:
            return await self.execute_workflow_sequential(workflow_id)
        elif workflow.workflow_type == WorkflowType.PARALLEL:
            return await self.execute_workflow_parallel(workflow_id)
        else:
            raise NotImplementedError(f"Workflow type {workflow.workflow_type} not implemented")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        task_statuses = {}
        for task in workflow.tasks:
            task_statuses[task.id] = {
                "status": task.status.value,
                "agent_type": task.agent_type,
                "method": task.method,
                "error": task.error,
                "created_at": task.created_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "workflow_type": workflow.workflow_type.value,
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "tasks": task_statuses,
            "results": workflow.results
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [
            {
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "status": workflow.status.value,
                "task_count": len(workflow.tasks)
            }
            for workflow in self.workflows.values()
        ]
    
    def list_agents(self) -> List[str]:
        """List all initialized agents"""
        return list(self.agents.keys())


# Convenience functions for common workflows
class WorkflowBuilder:
    """Helper class to build common workflows easily"""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
    
    def research_and_write_article(self, topic: str) -> str:
        """Create a workflow: Research -> Analyze -> Write -> Summarize"""
        workflow_id = self.orchestrator.create_workflow(
            name=f"Research and Write Article: {topic}",
            description=f"Research topic '{topic}', analyze findings, write article, and create summary",
            workflow_type=WorkflowType.SEQUENTIAL
        )
        
        # Research task
        research_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "researcher", "research", {"topic": topic}
        )
        
        # Analyze task (depends on research)
        analyze_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "analyzer", "analyze", 
            {"data": f"{{research_result}}", "analysis_type": "comprehensive"},
            dependencies=[research_task]
        )
        
        # Write task (depends on analysis)
        write_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "writer", "write_content",
            {"topic": topic, "content_type": "article"},
            dependencies=[analyze_task]
        )
        
        # Summarize task (depends on writing)
        self.orchestrator.add_task_to_workflow(
            workflow_id, "summarizer", "summarize",
            {"text": f"{{write_result}}", "max_length": "brief"},
            dependencies=[write_task]
        )
        
        return workflow_id
    
    def multi_language_content(self, topic: str, languages: List[str]) -> str:
        """Create a workflow for multi-language content creation"""
        workflow_id = self.orchestrator.create_workflow(
            name=f"Multi-language Content: {topic}",
            description=f"Create content about '{topic}' in multiple languages",
            workflow_type=WorkflowType.PARALLEL
        )
        
        # Write original content
        write_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "writer", "write_content", 
            {"topic": topic, "content_type": "article"}
        )
        
        # Create translation tasks in parallel
        for language in languages:
            self.orchestrator.add_task_to_workflow(
                workflow_id, "translator", "translate",
                {"text": f"{{write_result}}", "target_language": language},
                dependencies=[write_task]
            )
        
        return workflow_id
    
    def code_review_workflow(self, code: str, language: str = "python") -> str:
        """Create a workflow for code review and improvement"""
        workflow_id = self.orchestrator.create_workflow(
            name=f"Code Review: {language}",
            description=f"Review code, analyze findings, and create documentation",
            workflow_type=WorkflowType.SEQUENTIAL
        )
        
        # Review code
        review_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "code_reviewer", "review_code",
            {"code": code, "language": language}
        )
        
        # Analyze review findings
        analyze_task = self.orchestrator.add_task_to_workflow(
            workflow_id, "analyzer", "analyze",
            {"data": f"{{review_result}}", "analysis_type": "code review"},
            dependencies=[review_task]
        )
        
        # Create documentation
        self.orchestrator.add_task_to_workflow(
            workflow_id, "writer", "write_content",
            {"topic": f"Code Review Documentation for {language} code", "content_type": "documentation"},
            dependencies=[analyze_task]
        )
        
        return workflow_id
