# Updated System Architecture, Agent Roles, and Workflows

## System Architecture Overview

The system is composed of a backend and a frontend, with clearly defined components and agents to enable autonomous building, validation, and orchestration of software projects.

### Backend

- **backend/agents/**: Contains the core autonomous agents responsible for planning, building, validating, tool creation, and orchestration.
- **backend/tools/**: Base tools and dynamically generated tools for file operations and system interactions.
- **backend/core/**: Core modules including state management, configuration, and LLM interaction.
- **backend/memory/**: Persistent state storage and chat memory management.
- **backend/api.py**: FastAPI server providing API endpoints for frontend communication.
- **backend/main.py**: Main entry point to start the system.
- **backend/supervisor.py**: Supervisory agent managing overall system health and task scheduling.

### Frontend

- **frontend/**: Next.js UI components and pages for monitoring, control, and interaction with the system.

## Agent Roles

### OrchestratorAgent
- Core coordinator that manages the overall workflow.
- Maintains system mode (build vs working).
- Resumes interrupted build steps on startup.
- Delegates tasks to specialized agents.

### PlannerAgent
- Decomposes high-level goals into executable build steps.
- Plans task sequences and dependencies.

### BuilderAgent
- Writes and updates code files based on build steps.
- Handles code generation and modification.

### ValidatorAgent
- Validates generated code for correctness and quality.
- Runs tests and static analysis.

### ToolsmithAgent
- Creates new tools as needed to extend system capabilities.
- Manages tool lifecycle.

### ResearcherAgent (if present)
- Performs research tasks to gather information or generate knowledge.

### Scoring Agents
- Evaluate code and build steps for performance, safety, and unified scoring.

## Workflows

1. **Build Mode Activation**
   - Triggered by user command or system event.
   - OrchestratorAgent switches mode to "build".

2. **Planning**
   - PlannerAgent decomposes the build goal into steps.

3. **Building**
   - BuilderAgent executes build steps, writing code.

4. **Validation**
   - ValidatorAgent checks code correctness.

5. **Tool Creation**
   - ToolsmithAgent generates new tools if required.

6. **Resuming Interrupted Builds**
   - On startup, OrchestratorAgent resumes any interrupted build steps.

7. **Working Mode**
   - After build completion, system returns to "working" mode for normal operation.

## Notes

- The system maintains persistent state to enable crash recovery and task resumption.
- Agents communicate via shared state and orchestrator coordination.
- The architecture supports extensibility with new agents and tools.

---

This document should be updated as the system evolves to reflect new components and workflows.