import ast
from typing import List, Tuple

class SafetyScorerAgent:
    """Agent to analyze Python code for unsafe imports and usage patterns.
    Checks for subprocess with shell=True, eval, exec usage, and unsafe imports.
    """

    UNSAFE_IMPORTS = {"subprocess"}
    UNSAFE_FUNCTIONS = {"eval", "exec"}

    def __init__(self):
        pass

    def analyze_code(self, code: str) -> Tuple[int, List[str]]:
        """Analyze the given Python code and return a safety score and list of issues found.

        Args:
            code (str): Python source code to analyze.

        Returns:
            Tuple[int, List[str]]: safety score (0-100), list of issue descriptions.
        """
        issues = []
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Syntax error in code: {e}")
            return 0, issues

        # Check imports
        imports = self._find_imports(tree)
        for imp in imports:
            if imp in self.UNSAFE_IMPORTS:
                issues.append(f"Unsafe import detected: {imp}")

        # Check for unsafe function usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for eval or exec
                if isinstance(node.func, ast.Name) and node.func.id in self.UNSAFE_FUNCTIONS:
                    issues.append(f"Use of unsafe function: {node.func.id}")

                # Check for subprocess with shell=True
                if self._is_subprocess_shell_true(node):
                    issues.append("Use of subprocess with shell=True detected")

        # Calculate safety score
        score = 100
        penalty_per_issue = 20
        score -= penalty_per_issue * len(issues)
        if score < 0:
            score = 0

        return score, issues

    def _find_imports(self, tree: ast.AST) -> List[str]:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split('.')[0])
        return imports

    def _is_subprocess_shell_true(self, node: ast.Call) -> bool:
        # Check if the call is to subprocess.Popen or subprocess.call or subprocess.run with shell=True
        # We check if the function is an attribute of subprocess
        func = node.func
        if isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Name) and func.value.id == "subprocess":
                if func.attr in {"Popen", "call", "run"}:
                    # Check keywords for shell=True
                    for kw in node.keywords:
                        if kw.arg == "shell":
                            if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                return True
        return False


if __name__ == '__main__':
    sample_code = '''
import subprocess

def example(a, b, c, d, e, f):
    if a:
        for i in range(10):
            for j in range(10):
                if b:
                    print(i, j)
    global x
    eval('print(1)')
'''
    agent = SafetyScorerAgent()
    score, issues = agent.analyze_code(sample_code)
    print(f"Safety score: {score} / 100")
    for issue in issues:
        print(f"Issue: {issue}")
