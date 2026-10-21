import unittest
from evaluator import evaluate_response, run

class EvaluatorTests(unittest.TestCase):
    def test_all_rules_pass(self):
        rules = [{"type":"starts_with","value":"Answer:"},{"type":"exact_lines","value":2},{"type":"must_include","value":"privacy"}]
        self.assertEqual(evaluate_response("Answer: safe\nprivacy",rules)["score"],100)
    def test_required_term_missing(self):
        self.assertEqual(evaluate_response("hello",[{"type":"must_include","value":"world"}])["score"],0)
    def test_prohibited_term(self):
        self.assertEqual(evaluate_response("not guaranteed",[{"type":"must_not_include","value":"guaranteed"}])["score"],0)
    def test_tie(self):
        case={"id":"test","prompt":"test","rules":[{"type":"max_words","value":3}],"responses":{"A":"fine","B":"also fine"}}
        self.assertEqual(run([case])[0]["winner"],"tie")

if __name__ == "__main__":
    unittest.main()
