import backend.agents.scoring_agent as scoring_agent_module
import backend.agents.performance_scoring_agent as performance_scoring_agent_module
import backend.agents.safety_scorer as safety_scorer_module

class UnifiedScoringAgent:
    def __init__(self):
        self.quality_agent = scoring_agent_module.ScoringAgent()
        self.performance_agent = performance_scoring_agent_module.PerformanceScoringAgent()
        self.safety_agent = safety_scorer_module.SafetyScorerAgent()

    def score_code(self, code: str) -> dict:
        """
        Score the code using quality, performance, and safety agents.

        Returns:
            dict: {
                'total_score': float (0-10),
                'breakdown': {
                    'quality': {'score': float (0-10), 'issues': list},
                    'performance': {'score': float (0-10), 'issues': list},
                    'safety': {'score': float (0-10), 'issues': list}
                }
            }
        """
        quality_result = self.quality_agent.score_code(code)
        performance_result = self.performance_agent.analyze_code(code)
        safety_score, safety_issues = self.safety_agent.analyze_code(code)

        # Normalize scores from 0-100 to 0-10
        quality_score_10 = quality_result['total_score'] / 10
        performance_score_10 = performance_result['score'] / 10
        safety_score_10 = safety_score / 10

        # Combine scores equally weighted
        total_score = (quality_score_10 + performance_score_10 + safety_score_10) / 3

        return {
            'total_score': round(total_score, 2),
            'breakdown': {
                'quality': {
                    'score': round(quality_score_10, 2),
                    'issues': quality_result['issues']
                },
                'performance': {
                    'score': round(performance_score_10, 2),
                    'issues': performance_result.get('issues', [])
                },
                'safety': {
                    'score': round(safety_score_10, 2),
                    'issues': safety_issues
                }
            }
        }


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
    agent = UnifiedScoringAgent()
    result = agent.score_code(sample_code)
    print(f"Total Score (out of 10): {result['total_score']}")
    for category, details in result['breakdown'].items():
        print(f"\n{category.capitalize()} Score: {details['score']}")
        if details['issues']:
            print(f"Issues:")
            for issue in details['issues']:
                print(f" - {issue}")
        else:
            print("No issues detected.")
