import unittest
from analyzer.token_analysis import TokenAnalysis
from rich import print


class TestTokenAnalysis(unittest.TestCase):
    def setUp(self):
        self.token_analyzer = TokenAnalysis()

    def test_token_analysis(self):
        response = {
            'usage': {'input_tokens': 1000, 'output_tokens': 500},
            'model': 'claude-2.1'
        }
        total_cost = self.token_analyzer.token_analysis(response, 'ANTHROPIC')
        print(total_cost)
        self.assertIsNotNone(total_cost)


if __name__ == '__main__':
    unittest.main()
