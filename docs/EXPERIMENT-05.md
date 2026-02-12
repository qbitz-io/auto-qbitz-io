# EXPERIMENT-05: Orchestrator Recursion Fix & Cross-Codebase Integration Behavior

**Date:** 2026-02-11
**Branch:** `integration_qbitz_backend`
**Version:** Auto v1.0.3 (LangChain 1.0.3, gpt-4.1-mini)

---

## Part 1: Orchestrator Recursive Planning Spiral

### Problem

When Auto received a complex multi-part task (the qbitz_backend integration), the orchestrator decomposed it into phases via the Planner. But each phase was then re-evaluated by `_is_complex_prompt()`, which flags anything mentioning 2+ subsystem keywords (agents, tools, core, frontend, backend, api). Sub-phases like "Analyze the agents in qbitz_backend" naturally reference multiple subsystems, so they got flagged as complex, re-decomposed, and recursed until hitting the depth limit of 2.

**Result:** 59+ "Max recursion depth reached" failures, ~5% useful output, 10x baseline execution time.

### Root Cause

`_is_complex_prompt()` uses keyword counting to detect complexity:
```python
subsystems = ["agents", "tools", "core", "frontend", "backend", "api", "main entry point"]
subsystems_mentioned = sum(1 for s in subsystems if s in prompt.lower())
if subsystems_mentioned >= 2:
    return True
```

This heuristic doesn't distinguish between a top-level user request (which should be decomposed) and a sub-phase from the Planner (which is already decomposed and should execute directly).

### Fix

Three surgical edits to `backend/agents/orchestrator.py`, all in the `run()` method:

**1. Added `_is_phase` parameter to `run()`:**
```python
async def run(self, task: str, context: Optional[Dict[str, Any]] = None, depth: int = 0, _is_phase: bool = False) -> Dict[str, Any]:
```

**2. Skip complexity check when executing a phase:**
```python
if not _is_phase and self._is_complex_prompt(task):
```

**3. Pass `_is_phase=True` and previous phase results when executing sub-phases:**
```python
aggregated_results = []
for phase in phases:
    phase_context = {**full_context}
    if aggregated_results:
        phase_context["previous_phases"] = [
            {"phase": r["phase"], "result": r["result"].get("output", "")}
            for r in aggregated_results
        ]
    phase_result = await self.run(phase, context=phase_context, depth=depth+1, _is_phase=True)
    aggregated_results.append({"phase": phase, "result": phase_result})
```

### Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Recursion Errors | 59 | 0 | 100% eliminated |
| Phases Executed | 50+ (mostly failed) | 7 (all successful) | 100% success rate |
| Execution Time | 10x baseline | 1x baseline | 10x faster |
| Useful Output | ~5% | 100% | All output productive |

### Known Limitation

The `_is_complex_prompt()` heuristic itself is still too broad. Simple tasks that happen to mention two subsystem keywords will be unnecessarily decomposed. The `_is_phase` flag is a band-aid — the real fix would be replacing keyword counting with something smarter (e.g., LLM-based classification, or checking for multiple explicit action requests rather than keyword presence).

---

## Part 2: Cross-Codebase Integration — Behavioral Observations

### Setup

Auto was given the task of integrating agents, workflows, and tools from `../qbitz_backend` (a LangChain 0.3.27 + LangGraph social media agency platform) into his own system (LangChain 1.0.3).

### What Auto Did Well

**Analysis phase was excellent.** With the recursion fix in place, Auto produced a clean 7-phase report:
1. Analyzed all agents in qbitz_backend (SocialAgentFactory, 30+ specialized roles)
2. Analyzed workflow nodes (state transitions, agent-node mapping)
3. Analyzed workflow orchestration (LangGraph state graph, routing logic)
4. Identified integration points and 6 compatibility risks
5. Designed detailed integration plan with timeline
6. Self-reviewed the plan for feasibility
7. Presented final plan for approval

Each phase built on the previous one via the `previous_phases` context injection. The report was thorough and accurate.

**Auto correctly identified the key risks:**
- LangChain 0.3 vs 1.0 version incompatibility
- Different agent communication protocols
- Dependency conflicts (Firebase, Stripe, Runway)
- Tool interface mismatches

### Where Auto Failed

**Auto ignored his own plan during implementation.** Despite writing "need to align versions or create adapters" and "adapters or wrappers may be needed," Auto proceeded to:

1. **base_tools.py overwrite (DENIED):** Replaced the entire toolset with qbitz_backend's GPU-aware framework. Removed all actual tools (read_file, write_file, etc.), removed FileGuardian integration, removed Windows reserved filename checks, removed the `BASE_TOOLS` export. Would have bricked the system on startup.

2. **file_guardian.py overwrite (DENIED):** Replaced the full async approval system (~46 protected files, PendingApproval model, JSON persistence, API integration, frontend connection) with a 30-line stub containing only 2 protected files and no approval queue. Would have eliminated human-in-the-loop safety.

3. **planner.py overwrite — first attempt (DENIED):** Replaced the LLM-powered planner with a stub that split goals on the word "and." No LLM, no tools, no async, no state tracking. Would have broken the orchestrator.

4. **planner.py overwrite — second attempt (reviewed):** This time preserved the full existing planner and only added a `MAX_RECURSION_DEPTH` guard. Harmless but redundant — the recursion issue was already fixed in the orchestrator.

5. **social_agent_factory.py (unprotected, written directly):** Built a new file but used LangChain 0.3 import patterns (`from langchain.chat_models import ChatOpenAI`), wrong tool names (`read_file_tool` instead of `read_file`), missing `agent_scratchpad` placeholder, hardcoded model instead of `get_llm()`, and absolute imports instead of relative. Would crash at import time.

### Key Insight: Context Contamination

**The core failure pattern is context contamination.** When Auto reads source code from qbitz_backend and then immediately builds, the original code patterns persist in his context window. He can't "unsee" the 0.3 imports, the naming conventions, or the architectural patterns. He gravitates toward reproducing what he just read rather than building from what he already knows.

Evidence:
- He copied the factory pattern even though his existing agents don't use factories
- He used qbitz_backend's tool names (`read_file_tool`) instead of his own (`read_file`)
- He used 0.3 imports despite explicitly identifying the version gap in his analysis
- He attempted to replace core files rather than building alongside them

**This is a universal LLM behavior pattern:** when shown working code and asked to "build something inspired by it," the model treats the source as authoritative and reproduces its patterns, even when those patterns conflict with the target system.

### Proposed Solution: Two-Phase Context Isolation

To prevent context contamination in future integration work:

**Phase 1 — Read and Summarize (then discard):**
- Auto reads the source codebase
- Produces plain English specs for each component: what it does, its inputs/outputs, its role in the workflow
- **No implementation details** — no framework names, no version numbers, no import paths, no code snippets
- The spec describes behavior only: "An agent that handles client interaction, gathers requirements, and manages conversation stages"

**Phase 2 — Build from Spec (clean context):**
- Auto receives only the plain English spec
- Builds using his own established patterns (which already work)
- No reference to the source codebase
- The existing agents (orchestrator, planner, builder, validator) serve as his template — not the foreign code

This approach works because Auto already knows how to build excellent agents. His orchestrator, planner, and builder all follow clean LangChain 1.0 patterns with proper async, state management, and tool integration. He doesn't need implementation hints from a 0.3 codebase — he just needs to know what new agents to create.

---

## Part 3: FileGuardian Performance

FileGuardian proved its value during this experiment. Three dangerous overwrites were caught and denied:

| File | Risk | Caught |
|------|------|--------|
| `base_tools.py` | Would remove all tools + FileGuardian | Yes |
| `file_guardian.py` | Would remove approval system | Yes |
| `planner.py` (first attempt) | Would remove LLM planner | Yes |

**Gap identified:** `backend/agents/` is not protected. Auto wrote `social_agent_factory.py` directly without approval. While this particular file was harmless (broken but new), the agents directory contains critical files like `orchestrator.py` (which we had just patched). Consider adding key agent files to the protected list.

---

## Action Items

1. **Merge orchestrator recursion fix to stable v1.0.3** — the `_is_phase` flag and `previous_phases` context injection are proven and should be in the main branch
2. **Improve `_is_complex_prompt()` heuristic** — replace keyword counting with a smarter approach (future work)
3. **Implement two-phase context isolation** for any future cross-codebase integration tasks
4. **Review FileGuardian protected file list** — consider adding `backend/agents/orchestrator.py` and other critical agent files
5. **Document the "behavior-only spec" pattern** as a standard practice for teaching Auto new agent roles

---

## Commits

- `3dafd91` — Fix orchestrator recursive planning spiral (branch: `integration_qbitz_backend`)
