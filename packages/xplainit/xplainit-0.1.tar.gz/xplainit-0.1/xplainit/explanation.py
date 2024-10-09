import numpy as np
import matplotlib.pyplot as plt

class ExplainModel:
    def __init__(self, model):
        self.model = model

    def explain_prediction(self, feature_names, instance):
        """
        Generates a natural language explanation for a given model's prediction.
        """
        try:
            importances = self.model.feature_importances_
        except AttributeError:
            raise ValueError("Model does not support feature importance extraction")
        
        explanations = []
        for i, feature in enumerate(feature_names):
            explanations.append(f"The feature '{feature}' contributed {importances[i]:.2f} to the prediction.")

        explanation_text = " ".join(explanations)
        return f"The model's prediction is based on the following factors: {explanation_text}"

    def plot_feature_importance(self, feature_names):
        """
        Visualizes feature importance as a bar chart.
        """
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(8, 6))
        plt.barh(range(len(importances)), importances[indices], align='center')
        plt.yticks(range(len(importances)), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance in Model Prediction')
        plt.show()
