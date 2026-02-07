# Self-Building LangChain System

A self-extending, self-improving LangChain 1.0 system that can scaffold, reason about, and extend its own architecture.

## Architecture

### Backend (Python 3.11)
- **Orchestrator Agent**: Core agent responsible for planning, state tracking, and task dispatch
- **Specialized Agents**:
  - `PlannerAgent`: Decomposes goals into executable steps
  - `BuilderAgent`: Writes and updates Python and JS/TS files
  - `ValidatorAgent`: Runs static checks and validation on generated code
  - `ToolsmithAgent`: Creates new LangChain tools when gaps are detected
- **Persistent Memory**: Filesystem-based state tracking for build history and decisions

### Frontend (Next.js)
- Real-time build status dashboard
- Agent activity monitoring
- Reasoning summary streams
- Manual rebuild triggers

## Self-Build Loop

1. Inspect current repository state
2. Compare against desired system capabilities
3. Identify missing or broken components
4. Generate or repair code
5. Validate results
6. Persist updates
7. Terminate when no deltas detected

## Getting Started

### Backend Setup
```bash
cd backend
pip3 install -r requirements.txt
python3.11 main.py
```

### Frontend Setup
```bash
cd frontend
pnpm install
pnpm dev
```

## Environment Variables

Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_key_here
```

## System Capabilities

- Self-scaffolding from empty repository
- Architectural reasoning and introspection
- Dynamic capability extension through tool generation
- Automatic component detection and generation
- Persistent state across sessions
