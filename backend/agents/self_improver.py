"""SelfImprover agent - enhances system safety, intelligence, and self-improvement."""
from typing import Dict, Any
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..core import get_llm, state_manager, BuildStep
from ..tools import BASE_TOOLS
import uuid


SELF_IMPROVER_PROMPT = """You are the SelfImprover agent for a self-building LangChain system.

Your responsibilities:
1. Undo changes that break the system by reverting to last known good state.
2. Understand dependencies between components to avoid breaking the system.
3. Learn from build history and avoid repeating past mistakes.
4. Improve and refactor your own code for better quality and maintainability.
5. Generate tests to validate changes and ensure correctness.
6. Keep documentation synced with system evolution.

When performing tasks:
- Use system state and build history to inform decisions.
- Propose and execute undo operations if failures are detected.
- Analyze dependencies before making changes.
- Generate complete, executable code with tests and documentation updates.

Current system state:
- Project root: {project_root}
- Backend root: {backend_root}
- Generated files: {generated_files}
- Capabilities: {capabilities}
- Build history: {build_steps}

You have access to tools for:
- Reading and writing files
- Listing directories
- Validating Python syntax
- Running commands
- Checking system state
- Undoing changes
- Analyzing dependencies
- Generating tests
- Syncing documentation

Work systematically. Generate complete, executable code. No placeholders or TODOs.
"""


class SelfImproverAgent:
    """Agent that enhances system safety, intelligence, and self-improvement."""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
        self.tools = BASE_TOOLS
        self.agent_executor = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with tools."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", SELF_IMPROVER_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=25,
            handle_parsing_errors=True
        )
    
    async def improve(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform a self-improvement task.
        
        Args:
            task: Description of the improvement task
            context: Additional context
        
        Returns:
            Result of the improvement operation
        """
        # Get current state
        state = await state_manager.get_state()
        
        # Prepare context
        from ..core import settings
        full_context = {
            "project_root": str(settings.project_root),
            "backend_root": str(settings.backend_root),
            "generated_files": state.generated_files,
            "capabilities": [cap.model_dump() for cap in state.capabilities],
            "build_steps": [step.model_dump() for step in state.build_steps],
        }
        
        if context:
            full_context.update(context)
        
        # Create build step
        step_id = str(uuid.uuid4())
        step = BuildStep(
            id=step_id,
            agent="self_improver",
            action=task,
            status="running"
        )
        await state_manager.add_build_step(step)
        
        try:
            # Run agent
            result = await self.agent_executor.ainvoke({
                "input": task,
                **full_context
            })
            
            # Update step
            await state_manager.update_build_step(
                step_id,
                status="completed",
                result=str(result.get("output", ""))
            )
            
            return result
        
        except Exception as e:
            await state_manager.update_build_step(
                step_id,
                status="failed",
                error=str(e)
            )
            raise


# Global self-improver instance
self_improver = SelfImproverAgent()
