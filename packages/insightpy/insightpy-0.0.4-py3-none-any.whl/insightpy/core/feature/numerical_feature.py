
from insightpy.core.feature.base_feature import Feature
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr, spearmanr
from scipy.stats import shapiro, anderson
import pandas as pd
import numpy as np
from scipy.stats import levene
import textwrap

class NumericalFeature(Feature):

    def analyze(self):
        self.stats['single']={}
        self.stats['single']['mean']=self.data.mean()
        self.stats['single']['min']=self.data.min()
        self.stats['single']['max']=self.data.max()
        self.stats['single']['std']=self.data.std()
        self.stats['single']['skew']=self.data.skew()
        self.stats['single']['kurtosis']=self.data.kurtosis()
        self.stats['single']['normality']=self.normality_tests()

    def normality_tests(self):
        shapiro_test = shapiro(self.data)
        anderson_test = anderson(self.data)
        return {
            'shapiro_statistic': shapiro_test.statistic,
            'shapiro_p_value': shapiro_test.pvalue,
            'anderson_statistic': anderson_test.statistic,
            'anderson_critical_values': anderson_test.critical_values
        }

    def handle_skewness(self):
        feature=self.data
        skew_value = feature.skew()
        if skew_value > 1:
            transformed_feature = feature.apply(lambda x: np.log1p(x))  # Log transformation
            print(f'skew value is high {skew_value}, so we use log transformation')
        elif skew_value < -1:
            transformed_feature = feature.apply(lambda x: np.power(x, 2))  # Square transformation
            print(f'skew value is negative high {skew_value}, so we use square transformation x^2')
        else:
            transformed_feature = feature
        return transformed_feature




    def summary(self,target):

        """
        Generate a readable, pretty CLI summary of a numerical feature based on the provided statistics and analysis.

        :param feature_name: str, the name of the feature being analyzed
        :param feature_stats: dict, a dictionary containing all relevant metrics and tests for the feature
        :return: None, prints the summary directly to the CLI
        """

        self.analyze()
        self.handle_regression(target)
        feature_name=self.name
        feature_stats=self.stats
        summary = f"Feature: {feature_name} (Numerical)\n"
        summary += "=" * (len(summary) - 1) + "\n"

        # Basic Statistics
        summary += "Basic Statistics:\n"
        summary += f"  Mean: {feature_stats['single']['mean']:.4f}, Std Dev: {feature_stats['single']['std']:.4f}\n"#, Missing Values: {feature_stats['missing']}\n"
        summary += f"  Skewness: {feature_stats['single']['skew']:.4f}, Kurtosis: {feature_stats['single']['kurtosis']:.4f}\n"

        # Normality Test
        summary += "\nNormality Tests:\n"
        summary += f"  Shapiro-Wilk: Statistic = {feature_stats['single']['normality']['shapiro_statistic']:.4f}, p-value = {feature_stats['single']['normality']['shapiro_p_value']:.4f}\n"
        summary += f"  Anderson-Darling: Statistic = {feature_stats['single']['normality']['anderson_statistic']:.4f}, Critical Values = {feature_stats['single']['normality']['anderson_critical_values']}\n"

        # Dependency to Target
        summary += "\nDependency to Target (Correlation and Mutual Information):\n"
        summary += f"  Pearson Correlation: {feature_stats['n_target']['pearson_corr']:.4f}\n"
        summary += f"  Spearman Correlation: {feature_stats['n_target']['spearman_corr']:.4f}\n"
        summary += f"  Mutual Information: {feature_stats['n_target']['mutual_info']:.4f}\n"

        # Homoscedasticity Test
        summary += f"  Homoscedasticity (Levene’s Test): Statistic = {feature_stats['n_target']['levene_statistic']:.4f}, p-value = {feature_stats['n_target']['levene_p_value']:.4f}\n"

        # Outliers
        # summary += "\nOutliers:\n"
        # summary += f"  Outlier Count (Z-Score): {feature_stats['outliers_zscore']}, Outlier Count (IQR): {feature_stats['outliers_iqr']}\n"

        # Recommendations (based on computed values)
        summary += "\nRecommendations:\n"
        recommendations = []

        # Skewness analysis
        if feature_stats['single']['skew'] > 1:
            recommendations.append("  - Consider log or sqrt transformation to reduce high positive skewness.")
        elif feature_stats['single']['skew'] < -1:
            recommendations.append(
                "  - Consider squaring or cube-root transformation to reduce high negative skewness.")

        # Normality test analysis
        if feature_stats['single']['normality']['shapiro_p_value'] < 0.05:
            recommendations.append(
                "  - Data does not appear to follow a normal distribution (Shapiro test). Transformations or non-parametric models may help.")

        # Correlation vs Mutual Information
        if abs(feature_stats['n_target']['pearson_corr']) < 0.2 and feature_stats['n_target']['mutual_info'] > 0.2:
            recommendations.append(
                "  - Weak linear correlation but high mutual information. Consider using non-linear models (e.g., decision trees, boosting).")

        # Homoscedasticity analysis
        if feature_stats['n_target']['levene_p_value'] < 0.05:
            recommendations.append(
                "  - Violation of homoscedasticity detected (Levene’s Test). Consider weighted least squares regression.")

        # Final recommendations summary
        if not recommendations:
            recommendations.append(
                "  - No specific transformations or adjustments recommended based on the current analysis.")

        summary += "\n".join(recommendations) + "\n"

        # Print the summary in a pretty, wrapped format
        # print(textwrap.fill(summary, width=80))

        print(summary)

    def recommendation(self,target):
        self.analyze()
        self.handle_regression(target)
        feature_name = self.name
        feature_stats = self.stats
        summary = f"Feature: {feature_name}\n"
        summary += "=" * (len(summary) - 1) + "\n"
        # Recommendations (based on computed values)
        summary += "\nRecommendations:\n"
        recommendations = []

        # Skewness analysis
        if feature_stats['single']['skew'] > 1:
            recommendations.append("  - Consider log or sqrt transformation to reduce high positive skewness.")
        elif feature_stats['single']['skew'] < -1:
            recommendations.append(
                "  - Consider squaring or cube-root transformation to reduce high negative skewness.")

        # Normality test analysis
        if feature_stats['single']['normality']['shapiro_p_value'] < 0.05:
            recommendations.append(
                "  - Data does not appear to follow a normal distribution (Shapiro test). Transformations or non-parametric models may help.")

        # Correlation vs Mutual Information
        if abs(feature_stats['n_target']['pearson_corr']) < 0.2 and feature_stats['n_target']['mutual_info'] > 0.2:
            recommendations.append(
                "  - Weak linear correlation but high mutual information. Consider using non-linear models (e.g., decision trees, boosting).")

        # Homoscedasticity analysis
        if feature_stats['n_target']['levene_p_value'] < 0.05:
            recommendations.append(
                "  - Violation of homoscedasticity detected (Levene’s Test). Consider weighted least squares regression.")

        # Final recommendations summary
        if not recommendations:
            recommendations.append(
                "  - No specific transformations or adjustments recommended based on the current analysis.")

        summary += "\n".join(recommendations) + "\n"

        # Print the summary in a pretty, wrapped format
        # print(textwrap.fill(summary, width=80))

        # print(summary)
        return summary
    def detect_outliers(self, method='IQR'):
        """Stateless function that detects outliers in the feature data."""
        if method == 'IQR':
            q1 = self.data.quantile(0.25)
            q3 = self.data.quantile(0.75)
            iqr = q3 - q1
            return self.data[(self.data < (q1 - 1.5 * iqr)) | (self.data > (q3 + 1.5 * iqr))]



    def handle_regression(self, target:'NumericalTargetFeature'):
        """Handle numerical features by checking correlation, mutual information, and scaling."""
        # Check correlation
        valid_indices = self.data[~self.data.isin([np.inf, -np.inf]) & self.data.notna()].index

        # Filter both Series using the valid indices
        data_cleaned = self.data[valid_indices]
        target_cleaned = target.data[valid_indices]

        corr, _ = pearsonr(data_cleaned, target_cleaned)
        # print(f"Pearson Correlation with target: {corr}")
        self.stats['n_target']={}
        self.stats['n_target']['pearson_corr']=corr

        spearman_corr, _ = spearmanr(data_cleaned, target_cleaned)
        # print(f"Spearman Correlation with target: {spearman_corr}")
        self.stats['n_target']['spearman_corr'] = spearman_corr

        levene_stat, levene_p_value = levene(data_cleaned, target_cleaned)
        # print(f"homoscedasticity (levene) with target: {homoscedasticity}")
        self.stats['n_target']['levene_statistic'] = levene_stat
        self.stats['n_target']['levene_p_value'] = levene_p_value


        # Compute mutual information for non-linear relationships
        mi = mutual_info_regression(data_cleaned.values.reshape(-1, 1), target_cleaned.values.reshape(-1, 1))
        # print(f"Mutual Information: {mi[0]}")
        self.stats['n_target']['mutual_info'] = mi[0]

        # Non-linear transformation recommendation
        if corr < 0.2 and mi[0] > 0.5:
            # print("Suggesting log or sqrt transformation due to non-linear relationship.")
            # transformed_feature = np.log1p(self.data)  # Log transformation as an example
            pass

    def handle_numerical(self, target:Feature):
        """Handle numerical features by checking correlation, mutual information, and scaling."""
        # Check correlation
        if isinstance(target,NumericalFeature):
            corr, _ = pearsonr(self.data, target.data)
            print(f"Pearson Correlation with target: {corr}")
        else:
            corr, _ = spearmanr(self.data, target.data)
            print(f"Spearman Correlation with target: {corr}")

        # Compute mutual information for non-linear relationships
        mi = mutual_info_regression(self.data.values.reshape(-1, 1), target.data.values.reshape(-1, 1))
        print(f"Mutual Information: {mi[0]}")

        # Scaling
        scaler = StandardScaler()
        scaled_feature = scaler.fit_transform(self.data.values.reshape(-1, 1))

        # Non-linear transformation recommendation
        if corr < 0.2 and mi[0] > 0.5:
            print("Suggesting log or sqrt transformation due to non-linear relationship.")
            transformed_feature = np.log1p(self.data)  # Log transformation as an example

        return scaled_feature
