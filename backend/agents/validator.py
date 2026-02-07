"""Validator agent - runs static checks and logical validation on generated code."""
from typing import Dict, Any, List
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from ..core import get_llm, state_manager, BuildStep
from ..tools import BASE_TOOLS
import uuid


VALIDATOR_PROMPT = """You are the Validator agent for a self-building LangChain system.

Your responsibility is to validate generated code for correctness, quality, and consistency.

Validation checks:
1. Syntax validation (Python, JS/TS)
2. Import correctness
3. Type consistency
4. Logic errors
5. Best practices compliance
6. Security issues
7. Performance concerns

For Python files:
- Check syntax with validate_python_syntax tool
- Verify imports are available
- Check for common anti-patterns
- Ensure async/await is used correctly

For JavaScript/TypeScript files:
- Check for syntax errors
- Verify React component structure
- Check for missing dependencies

Output format:
- File path
- Validation status (PASS/FAIL)
- Issues found (if any)
- Severity (CRITICAL, WARNING, INFO)
- Suggested fixes

Be thorough but practical. Focus on issues that would prevent the system from running.

Generated files to validate: {generated_files}
"""


class ValidatorAgent:
    """Agent that validates generated code."""
    
    def __init__(self):
        self.llm = get_llm()
        self.tools = BASE_TOOLS
        self.agent_executor = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with tools."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", VALIDATOR_PROMPT),
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
    
    async def validate(self, target: str = None) -> Dict[str, Any]:
        """Validate code files.
        
        Args:
            target: Specific file to validate, or None to validate all generated files
        
        Returns:
            Validation results
        """
        # Get current state
        state = await state_manager.get_state()
        
        # Determine what to validate
        if target:
            task = f"Validate the file: {target}"
        else:
            task = "Validate all generated Python files in the backend directory"
        
        # Create build step
        step_id = str(uuid.uuid4())
        step = BuildStep(
            id=step_id,
            agent="validator",
            action=task,
            status="running"
        )
        await state_manager.add_build_step(step)
        
        try:
            # Run agent
            result = await self.agent_executor.ainvoke({
                "input": task,
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
    
    async def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a specific file.
        
        Args:
            file_path: Path to the file to validate
        
        Returns:
            Validation results
        """
        return await self.validate(target=file_path)


# Global validator instance
validator = ValidatorAgent()
