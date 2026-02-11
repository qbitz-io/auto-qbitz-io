"""Self-build loop - continuous system improvement cycle."""
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from .state import state_manager, SystemCapability
from .config import settings


class BuildLoop:
    """Manages the self-building loop."""
    
    def __init__(self):
        self.running = False
        self.iteration = 0
        self.max_iterations = 10  # Safety limit
        
    async def initialize_capabilities(self):
        """Initialize the list of required system capabilities."""
        state = await state_manager.get_state()
        
        # Define required capabilities
        required_capabilities = [
            SystemCapability(
                name="orchestrator_agent",
                description="Core orchestrator agent for planning and coordination",
                implemented=True,
                file_path="backend/agents/orchestrator.py"
            ),
            SystemCapability(
                name="planner_agent",
                description="Agent that decomposes goals into executable steps",
                implemented=True,
                file_path="backend/agents/planner.py"
            ),
            SystemCapability(
                name="builder_agent",
                description="Agent that writes and updates code files",
                implemented=True,
                file_path="backend/agents/builder.py"
            ),
            SystemCapability(
                name="validator_agent",
                description="Agent that validates generated code",
                implemented=True,
                file_path="backend/agents/validator.py"
            ),
            SystemCapability(
                name="toolsmith_agent",
                description="Agent that creates new tools",
                implemented=True,
                file_path="backend/agents/toolsmith.py"
            ),
            SystemCapability(
                name="base_tools",
                description="Base tools for file operations and system interaction",
                implemented=True,
                file_path="backend/tools/base_tools.py"
            ),
            SystemCapability(
                name="api_server",
                description="FastAPI server for frontend communication",
                implemented=False,
                file_path="backend/api.py"
            ),
            SystemCapability(
                name="main_entry",
                description="Main entry point for the system",
                implemented=False,
                file_path="backend/main.py"
            ),
            SystemCapability(
                name="frontend_ui",
                description="Next.js UI for monitoring and control",
                implemented=False,
                file_path="frontend/app/page.tsx"
            ),
        ]
        
        # Add capabilities if not already present
        existing_names = {cap.name for cap in state.capabilities}
        for cap in required_capabilities:
            if cap.name not in existing_names:
                await state_manager.add_capability(cap)
    
    async def inspect_repository(self) -> Dict[str, Any]:
        """Inspect current repository state.
        
        Returns:
            Repository state information
        """
        backend_path = settings.backend_root
        frontend_path = settings.project_root / "frontend"
        
        # Check what exists
        backend_files = []
        if backend_path.exists():
            for file in backend_path.rglob("*.py"):
                backend_files.append(str(file.relative_to(settings.project_root)))
        
        frontend_files = []
        if frontend_path.exists():
            for file in frontend_path.rglob("*.tsx"):
                frontend_files.append(str(file.relative_to(settings.project_root)))
            for file in frontend_path.rglob("*.ts"):
                if "node_modules" not in str(file):
                    frontend_files.append(str(file.relative_to(settings.project_root)))
        
        return {
            "backend_files": backend_files,
            "frontend_files": frontend_files,
            "backend_exists": backend_path.exists(),
            "frontend_exists": frontend_path.exists(),
        }
    
    async def identify_gaps(self) -> List[SystemCapability]:
        """Identify missing or broken components.
        
        Returns:
            List of unimplemented capabilities
        """
        # Get all capabilities
        state = await state_manager.get_state()
        
        # Check which files actually exist and update capability status
        gaps = []
        for cap in state.capabilities:
            if cap.file_path:
                full_path = settings.project_root / cap.file_path
                if full_path.exists():
                    # File exists, mark as implemented if not already
                    if not cap.implemented:
                        await state_manager.update_capability(cap.name, implemented=True, file_path=cap.file_path)
                else:
                    # File doesn't exist, it's a gap
                    gaps.append(cap)
            else:
                # No file path specified, check if implemented
                if not cap.implemented:
                    gaps.append(cap)
        
        return gaps
    
    async def generate_missing_components(self, gaps: List[SystemCapability]) -> bool:
        """Generate or repair missing components.
        
        Args:
            gaps: List of missing capabilities
        
        Returns:
            True if any components were generated
        """
        if not gaps:
            return False
        
        # Import here to avoid circular dependency
        from ..agents import orchestrator
        
        for gap in gaps:
            print(f"Generating component: {gap.name}")
            
            try:
                # Ask orchestrator to build the component
                result = await orchestrator.run(
                    f"Generate the missing component: {gap.name}. "
                    f"Description: {gap.description}. "
                    f"Target file: {gap.file_path}. "
                    f"Write complete, executable code."
                )
                
                # Mark as implemented
                await state_manager.update_capability(
                    gap.name,
                    implemented=True,
                    file_path=gap.file_path
                )
                
            except Exception as e:
                print(f"Error generating {gap.name}: {e}")
                continue
        
        return True
    
    async def validate_system(self) -> bool:
        """Validate the current system.
        
        Returns:
            True if validation passed
        """
        # Import here to avoid circular dependency
        from ..agents import validator
        
        try:
            result = await validator.validate()
            # Check if there are critical errors
            output = result.get("output", "")
            return "CRITICAL" not in output
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    async def run_cycle(self) -> bool:
        """Run one cycle of the build loop.
        
        Returns:
            True if changes were made, False if system is complete
        """
        self.iteration += 1
        print(f"\n=== Build Loop Iteration {self.iteration} ===\n")
        
        # Step 1: Inspect repository
        print("1. Inspecting repository...")
        repo_state = await self.inspect_repository()
        print(f"   Backend files: {len(repo_state['backend_files'])}")
        print(f"   Frontend files: {len(repo_state['frontend_files'])}")
        
        # Step 2: Identify gaps
        print("\n2. Identifying gaps...")
        gaps = await self.identify_gaps()
        print(f"   Found {len(gaps)} missing components")
        
        if not gaps:
            print("\n✓ No gaps found. System is complete!")
            return False
        
        for gap in gaps:
            print(f"   - {gap.name}: {gap.file_path}")
        
        # Step 3: Generate missing components
        print("\n3. Generating missing components...")
        changes_made = await self.generate_missing_components(gaps)
        
        # Step 4: Validate
        print("\n4. Validating system...")
        validation_passed = await self.validate_system()
        print(f"   Validation: {'PASSED' if validation_passed else 'FAILED'}")
        
        # Step 5: Persist state
        print("\n5. Persisting state...")
        await state_manager.save()
        
        return changes_made
    
    async def run(self):
        """Run the self-build loop until completion or max iterations."""
        self.running = True
        
        print("Starting self-build loop...")
        
        # Initialize capabilities
        await self.initialize_capabilities()
        
        try:
            while self.running and self.iteration < self.max_iterations:
                changes_made = await self.run_cycle()
                
                if not changes_made:
                    print("\n=== Build loop complete! ===")
                    break
                
                # Small delay between iterations
                await asyncio.sleep(1)
            
            if self.iteration >= self.max_iterations:
                print(f"\n⚠ Reached maximum iterations ({self.max_iterations})")
        
        finally:
            self.running = False
    
    def stop(self):
        """Stop the build loop."""
        self.running = False


# Global build loop instance
build_loop = BuildLoop()
