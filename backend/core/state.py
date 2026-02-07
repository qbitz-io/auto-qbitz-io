"""System state management and persistence."""
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from .config import settings


class BuildStep(BaseModel):
    """Represents a single build step in the system."""
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str
    action: str
    status: str  # pending, running, completed, failed
    result: Optional[str] = None
    error: Optional[str] = None


class SystemCapability(BaseModel):
    """Represents a capability the system should have."""
    name: str
    description: str
    implemented: bool = False
    file_path: Optional[str] = None


class SystemState(BaseModel):
    """Complete system state."""
    version: str = "0.1.0"
    last_updated: datetime = Field(default_factory=datetime.now)
    build_steps: List[BuildStep] = Field(default_factory=list)
    capabilities: List[SystemCapability] = Field(default_factory=list)
    generated_files: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StateManager:
    """Manages persistent system state."""
    
    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or (settings.memory_dir / "system_state.json")
        self._state: Optional[SystemState] = None
        self._lock = asyncio.Lock()
    
    async def load(self) -> SystemState:
        """Load state from disk or create new state."""
        async with self._lock:
            if self.state_file.exists():
                try:
                    with open(self.state_file, 'r') as f:
                        data = json.load(f)
                    self._state = SystemState(**data)
                except Exception as e:
                    print(f"Error loading state: {e}. Creating new state.")
                    self._state = SystemState()
            else:
                self._state = SystemState()
            
            return self._state
    
    async def save(self) -> None:
        """Save current state to disk."""
        async with self._lock:
            if self._state is None:
                return
            
            self._state.last_updated = datetime.now()
            
            with open(self.state_file, 'w') as f:
                json.dump(
                    self._state.model_dump(mode='json'),
                    f,
                    indent=2,
                    default=str
                )
    
    async def get_state(self) -> SystemState:
        """Get current state, loading if necessary."""
        if self._state is None:
            await self.load()
        return self._state
    
    async def add_build_step(self, step: BuildStep) -> None:
        """Add a build step to the state."""
        state = await self.get_state()
        state.build_steps.append(step)
        await self.save()
    
    async def update_build_step(self, step_id: str, status: str, result: Optional[str] = None, error: Optional[str] = None) -> None:
        """Update a build step's status."""
        state = await self.get_state()
        for step in state.build_steps:
            if step.id == step_id:
                step.status = status
                if result:
                    step.result = result
                if error:
                    step.error = error
                break
        await self.save()
    
    async def add_capability(self, capability: SystemCapability) -> None:
        """Add a system capability."""
        state = await self.get_state()
        state.capabilities.append(capability)
        await self.save()
    
    async def update_capability(self, name: str, implemented: bool, file_path: Optional[str] = None) -> None:
        """Update a capability's implementation status."""
        state = await self.get_state()
        for cap in state.capabilities:
            if cap.name == name:
                cap.implemented = implemented
                if file_path:
                    cap.file_path = file_path
                break
        await self.save()
    
    async def add_generated_file(self, file_path: str) -> None:
        """Track a generated file."""
        state = await self.get_state()
        if file_path not in state.generated_files:
            state.generated_files.append(file_path)
            await self.save()
    
    async def get_unimplemented_capabilities(self) -> List[SystemCapability]:
        """Get list of capabilities that need implementation."""
        state = await self.get_state()
        return [cap for cap in state.capabilities if not cap.implemented]


# Global state manager instance
state_manager = StateManager()
