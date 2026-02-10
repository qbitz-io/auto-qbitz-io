import ast

class CodeQualityVisitor(ast.NodeVisitor):
    """
    Visitor class to analyze Python AST nodes for code quality issues.

    Checks include:
    - Function length (too long functions)
    - Number of function arguments (too many arguments)
    - Nested block depth (too deep nesting)
    - Use of global statements
    - Class inheritance depth (too many base classes)
    """

    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node):
        # Check for long functions
        if hasattr(node, 'body') and len(node.body) > 50:
            self.issues.append((node.lineno, f"Function '{node.name}' is too long ({len(node.body)} statements)"))

        # Check for too many arguments
        if len(node.args.args) > 5:
            self.issues.append((node.lineno, f"Function '{node.name}' has too many arguments ({len(node.args.args)})"))

        # Check for nested blocks depth
        max_depth = self._max_nested_depth(node)
        if max_depth > 3:
            self.issues.append((node.lineno, f"Function '{node.name}' has too deep nesting ({max_depth})"))

        self.generic_visit(node)

    def visit_Global(self, node):
        self.issues.append((node.lineno, "Use of global statement"))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Check for deep inheritance
        if len(node.bases) > 3:
            self.issues.append((node.lineno, f"Class '{node.name}' has too many base classes ({len(node.bases)})"))
        self.generic_visit(node)

    def _max_nested_depth(self, node, current_depth=0):
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                child_depth = self._max_nested_depth(child, current_depth + 1)
                if child_depth > max_depth:
                    max_depth = child_depth
            else:
                child_depth = self._max_nested_depth(child, current_depth)
                if child_depth > max_depth:
                    max_depth = child_depth
        return max_depth

class ScoringAgent:
    """
    ScoringAgent evaluates Python code on multiple criteria and provides a composite score.

    Scoring Criteria and Methodology:

    1. Functionality (0 to 4 points):
       - Checks if the code parses without syntax errors.
       - If code parses, assigns a base score of 3.5 (good but not perfect).
       - If syntax errors are present, score is 0.

    2. Code Quality (0 to 2 points):
       - Analyzes code structure and style issues using AST analysis.
       - Issues checked include:
         * Long functions (>50 statements)
         * Functions with too many arguments (>5)
         * Deeply nested blocks (>3 levels)
         * Use of global statements
         * Classes with too many base classes (>3)
       - Starts with 2 points, subtracts 0.3 points per issue found, minimum 0.

    3. Performance (0 to 2 points):
       - Placeholder implementation currently returns full score (2.0).
       - Intended to be improved by a dedicated performance scoring agent.

    4. Safety (0 to 2 points):
       - Placeholder implementation currently returns full score (2.0).
       - Intended to be improved by a dedicated safety scoring agent.

    Total score ranges from 0 to 10 points.

    Usage:
    Instantiate ScoringAgent and call score_code(code_string) to get a detailed scoring report.

    Example:
        agent = ScoringAgent()
        result = agent.score_code(code_string)
        print(result['total_score'])
        print(result['criteria_scores'])
        print(result['issues'])
    """

    def __init__(self):
        pass

    def evaluate_functionality(self, code: str) -> float:
        """
        Evaluate the functionality of the code.
        Returns a score from 0 to 4.
        No automatic perfect score; if code parses, score is 3.5.
        """
        try:
            ast.parse(code)
            return 3.5  # good but not perfect
        except SyntaxError:
            return 0.0

    def evaluate_code_quality(self, code: str) -> (float, list):
        """
        Evaluate code quality by analyzing code structure and style issues.
        Returns score (0-2) and list of issues.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return 0.0, [(e.lineno, f'Syntax error: {e.msg}')]

        visitor = CodeQualityVisitor()
        visitor.visit(tree)
        issues = visitor.issues

        # Code quality scoring: start at 2 points, subtract 0.3 per issue, min 0
        score = max(0.0, 2.0 - 0.3 * len(issues))
        return score, issues

    def evaluate_performance(self, code: str) -> float:
        """
        Evaluate performance aspects of the code.
        Returns score from 0 to 2.
        Placeholder: returns 2.0 (full) - to be improved by performance agent.
        """
        return 2.0

    def evaluate_safety(self, code: str) -> float:
        """
        Evaluate safety aspects of the code.
        Returns score from 0 to 2.
        Placeholder: returns 2.0 (full) - to be improved by safety agent.
        """
        return 2.0

    def score_code(self, code: str):
        """
        Analyze the given Python code string and return a detailed score and list of issues.

        Returns:
            dict: {
                'total_score': float (0-10),
                'criteria_scores': {
                    'functionality': float,
                    'code_quality': float,
                    'performance': float,
                    'safety': float
                },
                'issues': list of (lineno, message) tuples
            }
        """
        functionality_score = self.evaluate_functionality(code)
        code_quality_score, issues = self.evaluate_code_quality(code)
        performance_score = self.evaluate_performance(code)
        safety_score = self.evaluate_safety(code)

        total_score = functionality_score + code_quality_score + performance_score + safety_score

        return {
            'total_score': round(total_score, 2),
            'criteria_scores': {
                'functionality': functionality_score,
                'code_quality': code_quality_score,
                'performance': performance_score,
                'safety': safety_score
            },
            'issues': issues
        }


if __name__ == '__main__':
    sample_code = '''
class Example:
    def method(self, a, b, c, d, e, f):
        if a:
            for i in range(10):
                if b:
                    print(i)
        global x
'''
    agent = ScoringAgent()
    result = agent.score_code(sample_code)
    print(f"Total Score: {result['total_score']} / 10")
    for criterion, score in result['criteria_scores'].items():
        print(f"{criterion.capitalize()} Score: {score}")
    for lineno, msg in result['issues']:
        print(f"Line {lineno}: {msg}")
