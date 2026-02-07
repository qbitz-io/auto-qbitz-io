# Architecture Documentation

## System Overview

The Self-Building LangChain System is a meta-system that can analyze, extend, and improve itself using LangChain 1.0 agents. It consists of a Python backend with specialized agents and a Next.js frontend for monitoring and control.

## Core Principles

### 1. Self-Awareness
The system maintains a persistent state of its own architecture, tracking:
- Implemented capabilities
- Generated files
- Build history
- System metadata

### 2. Self-Extension
Through the Toolsmith agent, the system can create new tools when it detects capability gaps.

### 3. Self-Validation
The Validator agent ensures all generated code is syntactically correct and follows best practices.

### 4. Persistence
All state is persisted to disk, allowing the system to resume from where it left off.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Status  │  │ Control  │  │Capabilit.│  │  Build   │   │
│  │  Panel   │  │  Panel   │  │  Panel   │  │  Steps   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  REST Endpoints  │  WebSocket  │  CORS Middleware    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Agent Layer (LangChain)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Orchestrator │  │   Planner    │  │   Builder    │     │
│  │    Agent     │  │    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  Validator   │  │  Toolsmith   │                        │
│  │    Agent     │  │    Agent     │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                      Tool Layer                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  read_file  │  write_file  │  validate_syntax  │ ... │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Core Infrastructure                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Config    │  │  State Mgr   │  │  Build Loop  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐                                           │
│  │  LLM Factory │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Persistence Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  File System  │  Memory Directory  │  State JSON     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Agent Specifications

### Orchestrator Agent

**Purpose**: Core coordination and high-level decision making

**Responsibilities**:
- Analyze system state
- Identify missing components
- Coordinate other agents
- Track build progress
- Decide when system is complete

**Tools Used**:
- All base tools
- Direct access to state manager

**Prompt Strategy**:
- System-aware: Knows project structure
- Goal-oriented: Focuses on completeness
- Delegating: Assigns work to specialized agents

### Planner Agent

**Purpose**: Decompose high-level goals into executable steps

**Responsibilities**:
- Break down complex goals
- Identify dependencies
- Assign agents to steps
- Define success criteria

**Tools Used**:
- Base tools for inspection
- State access for context

**Prompt Strategy**:
- Analytical: Understands requirements deeply
- Structured: Produces clear step-by-step plans
- Dependency-aware: Considers order of operations

### Builder Agent

**Purpose**: Write and update code files

**Responsibilities**:
- Generate Python code
- Generate JavaScript/TypeScript code
- Follow best practices
- Ensure completeness (no TODOs)

**Tools Used**:
- write_file
- read_file
- check_file_exists
- validate_python_syntax

**Prompt Strategy**:
- Quality-focused: Production-grade code only
- Complete: No placeholders or incomplete implementations
- Best practices: Follows language conventions

### Validator Agent

**Purpose**: Validate generated code

**Responsibilities**:
- Syntax checking
- Import verification
- Logic validation
- Best practices compliance

**Tools Used**:
- read_file
- validate_python_syntax
- run_command (for linting)

**Prompt Strategy**:
- Thorough: Checks multiple aspects
- Practical: Focuses on critical issues
- Actionable: Provides clear feedback

### Toolsmith Agent

**Purpose**: Create new tools when gaps are detected

**Responsibilities**:
- Identify capability gaps
- Design focused tools
- Generate tool code
- Integrate with system

**Tools Used**:
- write_file
- read_file
- validate_python_syntax

**Prompt Strategy**:
- Design-oriented: Thinks about tool interfaces
- Single-purpose: Creates focused tools
- Integration-aware: Ensures tools fit the system

## Data Flow

### Self-Build Loop Cycle

```
1. Initialize
   ↓
2. Load State
   ↓
3. Inspect Repository
   ↓
4. Identify Gaps
   ↓
5. Generate Components ──→ Orchestrator ──→ Builder
   ↓                                          ↓
6. Validate            ←──────────────────────┘
   ↓
7. Persist State
   ↓
8. Check Completion
   ↓
   ├─→ Gaps Found → Back to step 3
   └─→ No Gaps → Complete
```

### API Request Flow

```
Frontend Request
   ↓
FastAPI Endpoint
   ↓
State Manager (read state)
   ↓
Agent Execution
   ↓
Tool Calls
   ↓
State Manager (update state)
   ↓
Response to Frontend
```

### WebSocket Update Flow

```
State Change
   ↓
State Manager Save
   ↓
WebSocket Manager Broadcast
   ↓
Connected Clients Receive Update
   ↓
Frontend UI Updates
```

## State Management

### SystemState Model

```python
class SystemState(BaseModel):
    version: str
    last_updated: datetime
    build_steps: List[BuildStep]
    capabilities: List[SystemCapability]
    generated_files: List[str]
    metadata: Dict[str, Any]
```

### State Persistence

- **Format**: JSON
- **Location**: `backend/memory/system_state.json`
- **Update Strategy**: Immediate write after changes
- **Locking**: Async lock for concurrent access

### State Operations

- `load()` - Load from disk or create new
- `save()` - Persist to disk
- `add_build_step()` - Track agent actions
- `add_capability()` - Register new capabilities
- `update_capability()` - Mark as implemented
- `add_generated_file()` - Track generated files

## Tool Design

### Tool Characteristics

1. **Single Purpose**: Each tool does one thing well
2. **Type Safe**: Full type hints
3. **Async**: I/O operations are async
4. **Error Handling**: Graceful error messages
5. **Documented**: Clear docstrings for LLM

### Tool Template

```python
from langchain_core.tools import tool

@tool
async def tool_name(param: str) -> str:
    """Brief description for LLM.
    
    Args:
        param: Parameter description
    
    Returns:
        Return value description
    """
    try:
        # Implementation
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

## LLM Integration

### Model Configuration

- **Default Model**: gpt-4.1-mini
- **Temperature**: 0.0 (deterministic)
- **Builder Temperature**: 0.1 (slight creativity)

### Prompt Engineering

**Key Principles**:
1. **Context-Rich**: Provide current state
2. **Goal-Oriented**: Clear objectives
3. **Constraint-Aware**: Explicit limitations
4. **Tool-Aware**: Describe available tools

**Prompt Structure**:
```
System Role: Who the agent is
Responsibilities: What it should do
Current Context: System state
Available Tools: What it can use
Output Format: Expected structure
Quality Requirements: Standards to follow
```

## Error Handling

### Agent Errors

- Caught and logged in build steps
- Status set to "failed"
- Error message stored
- System continues with next component

### Tool Errors

- Return error message as string
- Agent can read and respond
- No system crash

### API Errors

- HTTP status codes
- JSON error responses
- Client-side error display

## Scalability Considerations

### Current Limitations

- Single-threaded agent execution
- In-memory state (with disk persistence)
- No distributed execution

### Future Enhancements

- Parallel agent execution
- Database-backed state
- Distributed task queue
- Caching layer for LLM responses

## Security Model

### Current Security

- Environment-based secrets
- CORS restrictions
- No authentication (development)

### Production Requirements

- API authentication
- Rate limiting
- Input sanitization
- Audit logging
- Secret management service

## Extension Points

### Adding New Agents

1. Create agent file in `backend/agents/`
2. Implement LangChain agent pattern
3. Add to `agents/__init__.py`
4. Register capability in build loop

### Adding New Tools

1. Use Toolsmith agent, or
2. Manually add to `backend/tools/`
3. Export from `tools/__init__.py`
4. Add to agent tool lists

### Adding New Capabilities

1. Define in `build_loop.initialize_capabilities()`
2. Specify file path and description
3. System will auto-detect implementation

## Testing Strategy

### Unit Testing

- Test individual tools
- Test state management
- Test agent initialization

### Integration Testing

- Test agent execution
- Test API endpoints
- Test build loop cycle

### End-to-End Testing

- Run full self-build
- Verify all capabilities implemented
- Test frontend integration

## Monitoring and Observability

### Metrics

- Build loop iterations
- Agent execution time
- Tool call frequency
- Error rates

### Logging

- Agent actions
- Tool calls
- State changes
- API requests

### Real-Time Updates

- WebSocket broadcasts
- Frontend dashboard
- Build step tracking
