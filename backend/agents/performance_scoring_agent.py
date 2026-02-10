import ast

class PerformanceScoringAgent:
    """
    Agent that analyzes Python code for performance issues or inefficiencies using static analysis.
    """

    def __init__(self):
        pass

    def analyze_code(self, code: str) -> dict:
        """
        Analyze the given Python code and return a performance report.

        Args:
            code (str): Python source code to analyze.

        Returns:
            dict: A report containing performance issues and a score (0-100).
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"score": 0, "issues": [f"Syntax error in code: {e}"]}

        issues = []

        # 1. Detect usage of nested loops (simple heuristic for inefficiency)
        nested_loops = self._count_nested_loops(tree)
        if nested_loops > 0:
            issues.append(f"Detected {nested_loops} nested loop(s), which may impact performance.")

        # 2. Detect large functions (more than 50 lines)
        large_functions = self._find_large_functions(tree, max_lines=50)
        for func_name, lines in large_functions:
            issues.append(f"Function '{func_name}' is large ({lines} lines), consider refactoring.")

        # 3. Detect usage of global variables (can impact performance and maintainability)
        globals_used = self._find_global_usage(tree)
        if globals_used:
            issues.append(f"Usage of global variables detected: {', '.join(globals_used)}.")

        # Calculate a simple performance score (100 - 15 points per issue)
        score = max(0, 100 - 15 * len(issues))

        return {
            "score": score,
            "issues": issues
        }

    def _count_nested_loops(self, tree: ast.AST) -> int:
        """Count nested for or while loops."""
        count = 0

        class LoopVisitor(ast.NodeVisitor):
            def __init__(self):
                self.nested_count = 0

            def visit_For(self, node):
                if any(isinstance(child, (ast.For, ast.While)) for child in ast.iter_child_nodes(node)):
                    self.nested_count += 1
                self.generic_visit(node)

            def visit_While(self, node):
                if any(isinstance(child, (ast.For, ast.While)) for child in ast.iter_child_nodes(node)):
                    self.nested_count += 1
                self.generic_visit(node)

        visitor = LoopVisitor()
        visitor.visit(tree)
        count = visitor.nested_count
        return count

    def _find_large_functions(self, tree: ast.AST, max_lines: int) -> list:
        """Find functions larger than max_lines."""
        large_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, 'body') and node.body:
                    start_line = node.lineno
                    end_line = max(getattr(n, 'lineno', start_line) for n in ast.walk(node))
                    length = end_line - start_line + 1
                    if length > max_lines:
                        large_funcs.append((node.name, length))
        return large_funcs

    def _find_global_usage(self, tree: ast.AST) -> list:
        """Detect usage of global variables."""
        globals_found = set()

        class GlobalVisitor(ast.NodeVisitor):
            def visit_Global(self, node):
                for name in node.names:
                    globals_found.add(name)

        visitor = GlobalVisitor()
        visitor.visit(tree)
        return list(globals_found)


if __name__ == '__main__':
    sample_code = '''
def example(a, b, c, d, e, f):
    if a:
        for i in range(10):
            for j in range(10):
                print(i, j)
    global x
'''
    agent = PerformanceScoringAgent()
    report = agent.analyze_code(sample_code)
    print(f"Performance score: {report['score']} / 100")
    for issue in report['issues']:
        print(f"Issue: {issue}")
