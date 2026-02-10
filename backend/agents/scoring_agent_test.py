from backend.agents.scoring_agent import ScoringAgent
import unittest

class TestScoringAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ScoringAgent()

    def test_valid_simple_function(self):
        code = """
def add(a, b):
    return a + b
"""
        result = self.agent.score_code(code)
        self.assertAlmostEqual(result['criteria_scores']['functionality'], 3.5)
        self.assertGreaterEqual(result['criteria_scores']['code_quality'], 1.7)
        self.assertEqual(len(result['issues']), 0)
        self.assertAlmostEqual(result['total_score'], 3.5 + result['criteria_scores']['code_quality'] + 2.0 + 2.0)

    def test_syntax_error(self):
        code = """
def broken_func(
    print("missing closing parenthesis")
"""
        result = self.agent.score_code(code)
        self.assertEqual(result['criteria_scores']['functionality'], 0.0)
        self.assertEqual(result['criteria_scores']['code_quality'], 0.0)
        self.assertTrue(any("Syntax error" in issue[1] for issue in result['issues']))
        self.assertLess(result['total_score'], 4.0)

    def test_long_function(self):
        code = "def long_func():\n" + "\n".join(["    x = 1"] * 51)
        result = self.agent.score_code(code)
        self.assertTrue(any("too long" in issue[1] for issue in result['issues']))
        self.assertLess(result['criteria_scores']['code_quality'], 2.0)

    def test_function_too_many_args(self):
        code = """
def many_args(a,b,c,d,e,f,g):
    pass
"""
        result = self.agent.score_code(code)
        self.assertTrue(any("too many arguments" in issue[1] for issue in result['issues']))

    def test_deep_nesting(self):
        code = """
def nested():
    if True:
        for i in range(1):
            while False:
                if True:
                    pass
"""
        result = self.agent.score_code(code)
        self.assertTrue(any("too deep nesting" in issue[1] for issue in result['issues']))

    def test_use_of_global(self):
        code = """
global x
x = 5
"""
        result = self.agent.score_code(code)
        self.assertTrue(any("Use of global statement" in issue[1] for issue in result['issues']))

    def test_class_too_many_bases(self):
        code = """
class MultiBase(A, B, C, D):
    pass
"""
        result = self.agent.score_code(code)
        self.assertTrue(any("too many base classes" in issue[1] for issue in result['issues']))

    def test_combined_issues(self):
        code = """
class MultiBase(A, B, C, D):
    def func(self, a,b,c,d,e,f):
        global x
        if True:
            for i in range(10):
                if True:
                    while False:
                        pass
""" + "\n".join(["    x = 1"] * 51)
        result = self.agent.score_code(code)
        self.assertTrue(len(result['issues']) >= 4)
        self.assertLess(result['criteria_scores']['code_quality'], 2.0)

if __name__ == '__main__':
    unittest.main()
