import ast
from typing import List, Tuple

class StaticCodeAnalyzer(ast.NodeVisitor):
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)
        self.issues: List[Tuple[int, int, str]] = []  # line, col, message

    def analyze(self) -> List[Tuple[int, int, str]]:
        """Perform static analysis and return list of issues found."""
        self.visit(self.tree)
        return self.issues

    def visit_Import(self, node: ast.Import):
        # Validate imports - example: disallow certain modules
        for alias in node.names:
            if alias.name in ('os', 'sys'):
                # Example: allow but warn about os and sys usage
                self.issues.append((node.lineno, node.col_offset, f"Use of import '{alias.name}' - ensure safe usage."))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        # Validate from imports
        if node.module in ('os', 'sys'):
            self.issues.append((node.lineno, node.col_offset, f"Use of from-import '{node.module}' - ensure safe usage."))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Detect eval and exec usage
        if isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec'):
                self.issues.append((node.lineno, node.col_offset, f"Use of '{node.func.id}' is a security risk."))

        # Detect subprocess calls with shell=True
        if isinstance(node.func, ast.Attribute):
            if (node.func.attr in ('Popen', 'call', 'run', 'check_call', 'check_output') and
                isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess'):
                # Check for shell=True in keywords
                for kw in node.keywords:
                    if kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value == True:
                        self.issues.append((node.lineno, node.col_offset, "Use of subprocess with shell=True is a security risk."))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Example anti-pattern: functions with too many arguments
        if len(node.args.args) > 10:
            self.issues.append((node.lineno, node.col_offset, f"Function '{node.name}' has too many arguments ({len(node.args.args)})."))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        # Example anti-pattern: classes with too many methods
        method_count = sum(isinstance(n, ast.FunctionDef) for n in node.body)
        if method_count > 20:
            self.issues.append((node.lineno, node.col_offset, f"Class '{node.name}' has too many methods ({method_count})."))
        self.generic_visit(node)

# Example usage function

def analyze_code(code: str) -> List[Tuple[int, int, str]]:
    analyzer = StaticCodeAnalyzer(code)
    return analyzer.analyze()

if __name__ == '__main__':
    sample_code = '''
import os
import subprocess

def dangerous():
    eval('print(123)')
    subprocess.run(['ls', '-l'], shell=True)

class BigClass:
    def m1(self): pass
    def m2(self): pass
    def m3(self): pass
    def m4(self): pass
    def m5(self): pass
    def m6(self): pass
    def m7(self): pass
    def m8(self): pass
    def m9(self): pass
    def m10(self): pass
    def m11(self): pass
'''
    issues = analyze_code(sample_code)
    for line, col, msg in issues:
        print(f"Line {line}, Col {col}: {msg}")
