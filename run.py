"""
Multi-Agent Orchestrator - Real AI Execution
"""

import asyncio
from orchestrator import MultiAgentOrchestrator, WorkflowBuilder, WorkflowType


async def main():
    print('🚀 Multi-Agent Orchestrator')
    print('=' * 40)
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    orchestrator.initialize_agents()
    
    # Create workflow
    workflow_id = orchestrator.create_workflow(
        name='Research and Write Pipeline',
        workflow_type=WorkflowType.SEQUENTIAL
    )
    
    # Add tasks
    task1 = orchestrator.add_task_to_workflow(
        workflow_id, 'researcher', 'research', {'topic': 'AI in Healthcare'}
    )
    
    task2 = orchestrator.add_task_to_workflow(
        workflow_id, 'writer', 'write_content', 
        {'topic': 'AI in Healthcare', 'content_type': 'article'},
        dependencies=[task1]
    )
    
    # Execute
    print('🔄 Executing workflow...')
    results = await orchestrator.execute_workflow(workflow_id)
    
    print(f'✅ Completed! Generated {len(results)} outputs')
    
    for task_id, result in results.items():
        print(f'\n📊 Result: {result}')


if __name__ == "__main__":
    asyncio.run(main())
