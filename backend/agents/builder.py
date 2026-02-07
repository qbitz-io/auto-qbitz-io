"""Builder agent - writes and updates Python and JS/TS files."""
from typing import Dict, Any
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..core import get_llm, state_manager, BuildStep
from ..tools import BASE_TOOLS
import uuid


BUILDER_PROMPT = """You are the Builder agent for a self-building LangChain system.

Your responsibility is to write and update code files (Python, JavaScript, TypeScript).

When given a build task:
1. Understand the requirements and context
2. Check if related files already exist
3. Write complete, production-ready code
4. Follow best practices and patterns
5. Ensure proper imports and dependencies
6. Add docstrings and type hints (Python)
7. Make code async-safe where applicable

Code quality requirements:
- NO placeholders or TODOs
- NO incomplete implementations
- Proper error handling
- Clear variable names
- Modular and maintainable

For Python:
- Use type hints
- Follow PEP 8
- Add docstrings
- Use async/await for I/O operations

For JavaScript/TypeScript:
- Use TypeScript when possible
- Follow modern ES6+ syntax
- Proper component structure for React

You have tools to:
- Read existing files
- Write new files
- Check if files exist
- Validate Python syntax
- List directories

Current project structure: {project_root}
Generated files: {generated_files}
"""


class BuilderAgent:
    """Agent that writes and updates code files."""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)  # Slightly higher for code generation
        self.tools = BASE_TOOLS
        self.agent_executor = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with tools."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", BUILDER_PROMPT),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=20,
            handle_parsing_errors=True
        )
    
    async def build(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a build task.
        
        Args:
            task: Description of what to build
            context: Additional context (file paths, requirements, etc.)
        
        Returns:
            Build result
        """
        # Get current state
        state = await state_manager.get_state()
        
        # Prepare context
        from ..core import settings
        full_context = {
            "project_root": str(settings.project_root),
            "generated_files": state.generated_files,
        }
        
        if context:
            full_context.update(context)
        
        # Create build step
        step_id = str(uuid.uuid4())
        step = BuildStep(
            id=step_id,
            agent="builder",
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


# Global builder instance
builder = BuilderAgent()
