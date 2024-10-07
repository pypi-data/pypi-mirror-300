from sklearn.feature_selection import mutual_info_classif
import numpy as np

# Interaction Analyzer class
class InteractionAnalyzer:
    @staticmethod
    def correlation(feature1, feature2):
        """Stateless function to calculate correlation between two numerical features."""
        return feature1.data.corr(feature2.data)

    @staticmethod
    def handle_interaction(feature1, feature2, target):
        """Handle interaction between two features."""
        # Compute correlation between the two features
        corr = np.corrcoef(feature1.data, feature2.data)[0, 1]
        print(f"Correlation between features: {corr}")

        # Mutual Information
        mi1 = mutual_info_classif(feature1.data.values.reshape(-1, 1), target.data)
        mi2 = mutual_info_classif(feature2.data.values.reshape(-1, 1), target.data)

        print(f"Mutual Information with target - Feature 1: {mi1[0]}, Feature 2: {mi2[0]}")

        # Interaction Suggestion
        if corr > 0.8:
            print("Suggesting to drop one feature due to high correlation.")
        elif mi1[0] > 0.5 and mi2[0] < 0.1:
            print("Feature 1 is significant, suggest using only Feature 1.")
        else:
            print("Creating interaction term between Feature 1 and Feature 2.")
            interaction = feature1.data * feature2.data  # Simple interaction term

        return interaction
