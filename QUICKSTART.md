# Quick Start Guide

Get the self-building LangChain system running in 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 22+
- pnpm
- OpenAI API key

## Installation

### 1. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip3 install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 2. Set Up Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
pnpm install
```

## Running the System

### Option A: Self-Build Mode

Run the self-building loop to let the system analyze and complete itself:

```bash
cd backend
python3.11 main.py
```

**Expected Output:**
```
============================================================
Self-Building LangChain System
============================================================

Loading system state...
Starting self-build loop...

=== Build Loop Iteration 1 ===

1. Inspecting repository...
2. Identifying gaps...
3. Generating missing components...
4. Validating system...
5. Persisting state...

✓ All capabilities implemented!
```

### Option B: API + Frontend Mode

**Terminal 1 - Start Backend API:**
```bash
cd backend
python3.11 api.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
pnpm dev
```

**Access the UI:**
Open http://localhost:3000 in your browser

## What You'll See

### Backend Console
- Build loop iterations
- Agent actions
- Component generation
- Validation results

### Frontend Dashboard
- **System Status**: Build loop state, capabilities progress
- **Control Panel**: Trigger/stop builds
- **Capabilities**: List of system components and their status
- **Build Steps**: Real-time log of agent actions

## First Steps

### 1. Explore the System State

```bash
curl http://localhost:8000/api/status | python3 -m json.tool
```

### 2. View Capabilities

```bash
curl http://localhost:8000/api/capabilities | python3 -m json.tool
```

### 3. Trigger a Build

```bash
curl -X POST http://localhost:8000/api/build \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

### 4. Execute a Custom Task

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Analyze the codebase and list all Python files",
    "context": {}
  }'
```

## Project Structure

```
self-building-langchain/
├── backend/
│   ├── agents/          # LangChain agents
│   │   ├── orchestrator.py
│   │   ├── planner.py
│   │   ├── builder.py
│   │   ├── validator.py
│   │   └── toolsmith.py
│   ├── core/            # Core infrastructure
│   │   ├── config.py
│   │   ├── state.py
│   │   ├── llm.py
│   │   └── build_loop.py
│   ├── tools/           # LangChain tools
│   │   └── base_tools.py
│   ├── memory/          # Persistent state
│   │   └── system_state.json
│   ├── api.py           # FastAPI server
│   ├── main.py          # Entry point
│   └── requirements.txt
├── frontend/
│   ├── app/             # Next.js pages
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── components/      # React components
│   │   ├── StatusPanel.tsx
│   │   ├── ControlPanel.tsx
│   │   ├── CapabilitiesPanel.tsx
│   │   └── BuildStepsPanel.tsx
│   └── package.json
├── README.md
├── ARCHITECTURE.md
├── DEPLOYMENT.md
└── QUICKSTART.md
```

## Key Concepts

### Agents

The system uses 5 specialized LangChain agents:

1. **Orchestrator** - Coordinates the system
2. **Planner** - Breaks down goals
3. **Builder** - Generates code
4. **Validator** - Checks code quality
5. **Toolsmith** - Creates new tools

### Self-Building Loop

The system can:
1. Inspect its own codebase
2. Identify missing components
3. Generate code to fill gaps
4. Validate the generated code
5. Persist changes
6. Repeat until complete

### Capabilities

The system tracks 9 core capabilities:
- Orchestrator agent
- Planner agent
- Builder agent
- Validator agent
- Toolsmith agent
- Base tools
- API server
- Main entry point
- Frontend UI

## Common Tasks

### Add a New Capability

Edit `backend/core/build_loop.py`:

```python
SystemCapability(
    name="my_new_feature",
    description="Description of the feature",
    implemented=False,
    file_path="backend/my_feature.py"
)
```

Run the build loop to generate it:

```bash
python3.11 main.py
```

### Create a New Tool

Use the Toolsmith agent via API:

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a tool that counts lines of code in a file",
    "context": {}
  }'
```

### Extend an Agent

1. Edit the agent file in `backend/agents/`
2. Modify the prompt or add tools
3. Restart the API server

## Troubleshooting

### "Failed to fetch" in Frontend

**Problem**: Frontend can't connect to backend

**Solution**: 
1. Ensure backend is running on port 8000
2. Check `http://localhost:8000/api/status` in browser
3. Verify CORS settings in `backend/api.py`

### "ImportError: attempted relative import"

**Problem**: Python can't resolve imports

**Solution**:
```bash
# Run from project root
cd /path/to/self-building-langchain
PYTHONPATH=$(pwd) python3.11 backend/main.py
```

### Build Loop Finds No Gaps

**Problem**: System thinks it's complete but files are missing

**Solution**:
1. Delete `backend/memory/system_state.json`
2. Run `python3.11 main.py` again
3. System will reinitialize and detect gaps

### OpenAI API Errors

**Problem**: Rate limits or authentication errors

**Solution**:
1. Check your API key in `.env`
2. Verify you have credits
3. Consider using a different model in `backend/core/config.py`

## Next Steps

1. **Read the Architecture**: See `ARCHITECTURE.md` for system design
2. **Deploy to Production**: See `DEPLOYMENT.md` for deployment guide
3. **Extend the System**: Add new agents, tools, or capabilities
4. **Monitor Performance**: Use the dashboard to track system behavior

## Getting Help

- Check the documentation in the `docs/` directory
- Review the code comments
- Examine the system state in `backend/memory/system_state.json`
- Use the API to query system status

## Example Workflow

```bash
# 1. Start backend
cd backend
python3.11 api.py &

# 2. Start frontend
cd frontend
pnpm dev &

# 3. Open browser
open http://localhost:3000

# 4. Trigger a build from UI
# Click "Trigger Build" button

# 5. Watch the system work
# Observe build steps in real-time

# 6. Check results
curl http://localhost:8000/api/status

# 7. Execute custom task
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"task": "List all implemented capabilities"}'
```

## Success Indicators

✅ Backend API responds on port 8000  
✅ Frontend loads on port 3000  
✅ All 9 capabilities show as "implemented"  
✅ Build loop completes without errors  
✅ Dashboard displays system status  
✅ Custom tasks execute successfully  

Congratulations! Your self-building LangChain system is now running.
