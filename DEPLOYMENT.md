# Deployment Guide

## Prerequisites

- Python 3.11
- Node.js 22+
- pnpm
- OpenAI API key

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Self-Build Loop

The system can analyze itself and ensure all components are present:

```bash
cd backend
python3.11 main.py
```

Expected output:
```
============================================================
Self-Building LangChain System
============================================================

Loading system state...
State loaded: 9 capabilities, 0 files

Starting self-build loop...

=== Build Loop Iteration 1 ===

1. Inspecting repository...
   Backend files: 16
   Frontend files: 8

2. Identifying gaps...
   Found 0 missing components

✓ No gaps found. System is complete!

=== Build loop complete! ===
```

### 4. Start the API Server

```bash
cd backend
python3.11 api.py
```

The API will be available at `http://localhost:8000`

**API Endpoints:**
- `GET /api/status` - System status
- `GET /api/capabilities` - List of capabilities
- `GET /api/build-steps` - Recent build steps
- `GET /api/files` - Generated files
- `POST /api/build` - Trigger build cycle
- `POST /api/build/stop` - Stop build cycle
- `POST /api/task` - Execute custom task
- `WS /ws` - WebSocket for real-time updates

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
pnpm install
```

### 2. Start Development Server

```bash
pnpm dev
```

The UI will be available at `http://localhost:3000`

### 3. Production Build

```bash
pnpm build
pnpm start
```

## Architecture Overview

### Backend Components

**Core Infrastructure (`backend/core/`)**
- `config.py` - Configuration management
- `state.py` - State persistence
- `llm.py` - LLM initialization
- `build_loop.py` - Self-building loop logic

**Agents (`backend/agents/`)**
- `orchestrator.py` - Core coordination agent
- `planner.py` - Goal decomposition
- `builder.py` - Code generation
- `validator.py` - Code validation
- `toolsmith.py` - Tool creation

**Tools (`backend/tools/`)**
- `base_tools.py` - File operations, validation, system state

**API (`backend/api.py`)**
- FastAPI server for frontend communication
- RESTful endpoints
- WebSocket support

**Entry Point (`backend/main.py`)**
- Self-build loop execution
- System initialization

### Frontend Components

**Pages (`frontend/app/`)**
- `page.tsx` - Main dashboard
- `layout.tsx` - App layout

**Components (`frontend/components/`)**
- `StatusPanel.tsx` - System status display
- `ControlPanel.tsx` - Build controls
- `CapabilitiesPanel.tsx` - Capabilities list
- `BuildStepsPanel.tsx` - Build history

## Usage

### Running the Self-Build Loop

```bash
cd backend
python3.11 main.py
```

This will:
1. Load existing system state
2. Inspect the repository
3. Identify missing components
4. Generate or repair code
5. Validate results
6. Persist updates

### Using the API

Start the backend server:
```bash
cd backend
python3.11 api.py
```

Trigger a build cycle:
```bash
curl -X POST http://localhost:8000/api/build \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

Check system status:
```bash
curl http://localhost:8000/api/status
```

### Using the UI

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. View system status, capabilities, and build steps
4. Trigger builds using the control panel

## System Capabilities

The system tracks these capabilities:

1. **orchestrator_agent** - Core coordination
2. **planner_agent** - Goal decomposition
3. **builder_agent** - Code generation
4. **validator_agent** - Code validation
5. **toolsmith_agent** - Tool creation
6. **base_tools** - File operations
7. **api_server** - REST API
8. **main_entry** - Entry point
9. **frontend_ui** - Dashboard UI

## Extending the System

### Adding New Tools

Use the Toolsmith agent to create new tools:

```python
from backend.agents import toolsmith

result = await toolsmith.create_tool(
    "Create a tool that analyzes Python code complexity"
)
```

### Adding New Capabilities

Edit `backend/core/build_loop.py` and add to `initialize_capabilities()`:

```python
SystemCapability(
    name="new_capability",
    description="Description of the capability",
    implemented=False,
    file_path="path/to/file.py"
)
```

### Custom Tasks

Execute custom tasks via the API:

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the current codebase and suggest improvements",
    "context": {}
  }'
```

## Troubleshooting

### Import Errors

If you see `ImportError: attempted relative import beyond top-level package`:

Make sure you're running from the correct directory or using the proper Python path:

```bash
cd /path/to/self-building-langchain
PYTHONPATH=/path/to/self-building-langchain python3.11 backend/main.py
```

### API Connection Issues

If the frontend can't connect to the backend:

1. Ensure the backend is running on port 8000
2. Check CORS settings in `backend/api.py`
3. Verify the API_BASE URL in `frontend/app/page.tsx`

### Build Loop Not Finding Gaps

The build loop automatically marks existing files as implemented. To force regeneration:

1. Delete the file you want to regenerate
2. Update the capability status in `backend/memory/system_state.json`
3. Run the build loop again

## Production Deployment

### Backend

Use a production ASGI server:

```bash
pip install gunicorn
gunicorn backend.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

Build and serve:

```bash
cd frontend
pnpm build
pnpm start
```

Or use a static hosting service:

```bash
pnpm build
# Deploy the .next/static folder to your CDN
```

### Environment Variables

Set these in production:

```env
OPENAI_API_KEY=your_production_key
OPENAI_MODEL=gpt-4.1-mini
API_HOST=0.0.0.0
API_PORT=8000
```

## Security Considerations

1. **API Keys**: Never commit `.env` files to version control
2. **CORS**: Restrict `allow_origins` in production
3. **Rate Limiting**: Add rate limiting to API endpoints
4. **Authentication**: Add authentication for production use
5. **Input Validation**: Validate all user inputs

## Performance Optimization

1. **Caching**: Cache LLM responses for repeated queries
2. **Async Operations**: All I/O operations are async
3. **Connection Pooling**: Use connection pooling for database operations
4. **Frontend**: Use React Server Components where possible

## Monitoring

The system provides real-time monitoring through:

1. **WebSocket Updates**: Real-time state changes
2. **Build Steps**: Historical record of all actions
3. **Capabilities Tracking**: Implementation status
4. **Error Logging**: Comprehensive error tracking
