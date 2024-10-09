import unittest
from sklearn.ensemble import RandomForestClassifier
from xplainit.explanation import ExplainModel

class TestExplainModel(unittest.TestCase):
    def setUp(self):
        self.model = RandomForestClassifier()
        self.model.fit([[1, 2], [2, 3], [3, 4]], [0, 1, 0])
        self.explainer = ExplainModel(self.model)

    def test_explain_prediction(self):
        explanation = self.explainer.explain_prediction(['feature1', 'feature2'], [2, 3])
        self.assertIn("The feature", explanation)

if __name__ == "__main__":
    unittest.main()
