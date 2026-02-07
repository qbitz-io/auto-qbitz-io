"""Planner agent - decomposes goals into executable steps."""
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..core import get_llm, state_manager, BuildStep
from ..tools import BASE_TOOLS
import uuid


PLANNER_PROMPT = """You are the Planner agent for a self-building LangChain system.

Your responsibility is to decompose high-level goals into concrete, executable steps.

When given a goal:
1. Break it down into logical, sequential steps
2. Identify dependencies between steps
3. Specify which agent should handle each step (Builder, Validator, Toolsmith)
4. Ensure steps are atomic and testable
5. Consider the current system state

Output format:
For each step, provide:
- Step number
- Description
- Responsible agent
- Dependencies (which steps must complete first)
- Success criteria

Be specific and actionable. Each step should be clear enough that another agent can execute it without ambiguity.

Current system capabilities: {capabilities}
Generated files: {generated_files}
"""


class PlannerAgent:
    """Agent that decomposes goals into executable steps."""
    
    def __init__(self):
        self.llm = get_llm()
        self.tools = BASE_TOOLS
        self.agent_executor = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with tools."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", PLANNER_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=15,
            handle_parsing_errors=True
        )
    
    async def plan(self, goal: str) -> Dict[str, Any]:
        """Create a plan for achieving a goal.
        
        Args:
            goal: The high-level goal to plan for
        
        Returns:
            Plan with executable steps
        """
        # Get current state
        state = await state_manager.get_state()
        
        # Create build step
        step_id = str(uuid.uuid4())
        step = BuildStep(
            id=step_id,
            agent="planner",
            action=f"Plan: {goal}",
            status="running"
        )
        await state_manager.add_build_step(step)
        
        try:
            # Run agent
            result = await self.agent_executor.ainvoke({
                "input": f"Create a detailed plan to achieve this goal: {goal}",
                "capabilities": [cap.model_dump() for cap in state.capabilities],
                "generated_files": state.generated_files,
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


# Global planner instance
planner = PlannerAgent()
