from scipy.stats import zscore
import numpy as np

from insightpy.core.feature import Feature


class OutlierAnalyzer:

    @staticmethod
    def handle_outliers_and_scaling(feature:Feature):
        """Handle outliers and scaling of numerical features."""
        # Z-score for outlier detection
        z_scores = zscore(feature.data)
        outliers = np.where(np.abs(z_scores) > 3)[0]  # Threshold of 3 for detecting outliers
        print(f"Outliers detected at indices: {outliers}")

        # Winsorization for capping outliers
        capped_feature = np.clip(feature.data, feature.data.quantile(0.01), feature.data.quantile(0.99))

        # Scaling the feature
        scaled_feature = (capped_feature - capped_feature.mean()) / capped_feature.std()

        return scaled_feature
