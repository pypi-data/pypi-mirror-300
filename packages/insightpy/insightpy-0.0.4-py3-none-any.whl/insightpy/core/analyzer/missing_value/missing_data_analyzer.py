import pandas as pd

# Missing Data Analyzer
class MissingDataAnalyzer:
    @staticmethod
    def analyze_missing_data(feature, target=None):
        """Stateless function to analyze missing data for a feature."""
        if target is None:
            return feature.data.isnull().sum()  # Univariate missing data analysis
        else:
            return MissingDataAnalyzer._missing_vs_target(feature, target)

    @staticmethod
    def _missing_vs_target(feature, target):
        """Analyze missing data and its correlation with the target."""
        return pd.crosstab(feature.data.isnull(), target.data)