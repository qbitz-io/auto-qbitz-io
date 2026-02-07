"""Tools to support self-improvement capabilities: undo, dependency analysis, test generation, documentation sync."""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.tools import tool


@tool
async def undo_last_change() -> str:
    """Undo the last change by restoring files from backup or version control.

    Returns:
        Status message
    """
    # For simplicity, assume backups are stored in memory/backup/
    backup_dir = Path("backend/memory/backup")
    project_root = Path("backend")
    if not backup_dir.exists():
        return "No backup directory found. Cannot undo."

    # Copy files from backup to project root
    for root, dirs, files in os.walk(backup_dir):
        rel_path = Path(root).relative_to(backup_dir)
        target_dir = project_root / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            src_file = Path(root) / file
            dst_file = target_dir / file
            shutil.copy2(src_file, dst_file)

    return "Undo completed: restored files from backup."


@tool
def analyze_dependencies() -> Dict[str, List[str]]:
    """Analyze Python files in backend/agents and backend/tools to build a dependency graph.

    Returns:
        Dictionary mapping file paths to list of dependencies (imported modules/files).
    """
    import ast
    from pathlib import Path

    base_dirs = [Path("backend/agents"), Path("backend/tools")]
    dependency_graph = {}

    for base_dir in base_dirs:
        for py_file in base_dir.rglob("*.py"):
            try:
                with open(py_file, "r") as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                dependency_graph[str(py_file)] = imports
            except Exception as e:
                dependency_graph[str(py_file)] = [f"Error parsing: {e}"]

    return dependency_graph


@tool
async def generate_tests_for_file(file_path: str) -> str:
    """Generate test code for a given Python file.

    Args:
        file_path: Path to the Python file to generate tests for

    Returns:
        Status message
    """
    # For demonstration, generate a simple pytest stub
    test_file_path = Path(file_path).parent / f"test_{Path(file_path).name}"
    test_code = f"""import pytest

# Auto-generated tests for {file_path}

def test_placeholder():
    assert True
"""
    with open(test_file_path, "w") as f:
        f.write(test_code)
    return f"Generated test file: {test_file_path}"


@tool
async def sync_documentation() -> str:
    """Sync documentation files with current system state.

    Returns:
        Status message
    """
    # For demonstration, update README.md with current capabilities
    from ..core import state_manager
    import asyncio

    state = asyncio.run(state_manager.get_state())
    capabilities = state.capabilities

    readme_path = Path("README.md")
    lines = ["# System Capabilities\n"]
    for cap in capabilities:
        status = "Implemented" if cap.implemented else "Pending"
        lines.append(f"- {cap.name}: {cap.description} [{status}]\n")

    with open(readme_path, "w") as f:
        f.writelines(lines)

    return "Documentation synced with current capabilities."
