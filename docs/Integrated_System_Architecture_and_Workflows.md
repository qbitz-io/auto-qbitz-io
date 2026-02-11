# Integrated System Architecture and Workflows

## 1. System Architecture

### Backend Structure

- **backend/agents/**: Contains core agents responsible for planning, building, validating, tool creation, orchestration, and research.
  - PlannerAgent: Decomposes high-level goals into executable steps.
  - BuilderAgent: Writes and updates code files.
  - ValidatorAgent: Validates generated code for correctness and safety.
  - ToolsmithAgent: Creates new tools dynamically as needed.
  - OrchestratorAgent: Core orchestrator managing planning, building, validation, and mode transitions.
  - ResearcherAgent: Supports research and information gathering.
  - Scoring Agents: PerformanceScoringAgent, SafetyScorer, UnifiedScoringAgent for evaluating code quality and safety.
  - StaticCodeAnalyzer: Performs static analysis on code.

- **backend/tools/**: Base tools for file operations and system interaction, plus dynamically generated tools.

- **backend/core/**: Core infrastructure including:
  - `state.py`: Manages persistent state, including build steps and their statuses.
  - `file_guardian.py`: Protects critical files from unauthorized changes.
  - `config.py` (if present): Configuration management.
  - `llm.py` (if present): Language model interface.

- **backend/memory/**: Persistent state storage, e.g., chat memory.

- **backend/api.py**: FastAPI server providing API endpoints for frontend communication.

- **backend/main.py**: Main entry point initializing the system and starting the API server.

### Frontend Structure

- **frontend/**: Next.js UI for monitoring, control, and interaction.
  - Components like `ChatInterface.tsx` provide user interaction.
  - Pages such as `app/page.tsx` serve as entry points.

## 2. Updated Workflows

### Build Mode vs Working Mode

- The system operates in two modes:
  - **Build Mode**: Active when the system is executing a build task (planning, coding, validating).
  - **Working Mode**: Default mode for normal operation and interaction.

- Mode is managed by the OrchestratorAgent via a `mode` attribute.
- Commands like "Auto, build me a ..." switch the system into build mode.
- Upon build completion or failure, the system returns to working mode.

### Task Resume Capability

- On startup, the StateManager marks stale "running" build steps as "interrupted".
- OrchestratorAgent queries for interrupted steps and resumes them automatically.
- This ensures recovery from crashes or unexpected shutdowns without losing progress.

### Agent Interaction and Coordination

- OrchestratorAgent coordinates the workflow:
  - Receives high-level goals.
  - Uses PlannerAgent to decompose goals.
  - Delegates code writing to BuilderAgent.
  - Validates code via ValidatorAgent.
  - Requests new tools from ToolsmithAgent as needed.
  - Uses scoring agents to evaluate code quality and safety.

- Agents communicate via shared state and method calls.

### Toolsmith Dynamic Tool Creation

- ToolsmithAgent creates new tools dynamically based on system needs.
- Tools are added to `backend/tools/` and integrated into workflows.

### Validation and Scoring

- ValidatorAgent ensures code correctness and safety.
- Scoring agents provide quantitative assessments.
- StaticCodeAnalyzer performs static checks.

## 3. Migration Changes

### Integration of ../qbitz-backend Agents and Workflows

- Replaced or refactored existing agents to align with the new architecture.
- Adopted new workflows emphasizing mode management and task resumption.

### State Management Updates

- Enhanced StateManager to support querying build steps by status.
- Improved persistence and recovery mechanisms.

### Dependency and Environment

- Added `pytest` to requirements for testing.
- Updated environment to support new dependencies.

### Testing and Validation

- Added tests for agents and workflows.
- Validated Python syntax and system behavior.

---

This document summarizes the integrated system architecture and workflows after migration from ../qbitz-backend. The system now supports robust build and working modes, task resumption, dynamic tool creation, and comprehensive validation and scoring.
