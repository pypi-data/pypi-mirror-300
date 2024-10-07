from insightpy.core.feature.base_feature import Feature
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import chi2_contingency, f_oneway
import pandas as pd
import pandas as pd
from scipy.stats import f_oneway, kruskal, chi2_contingency
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import textwrap
class CategoricalFeature(Feature):
    def summary(self,target):
        return {}

    def analyze(self):
        self.stats['single']={}
        self.stats['single']['categories']= self.data.unique()
        self.stats['single']['missing_values']=self.data.isnull().sum()
        self.stats['single']['frequency']=self.data.value_counts()

    def handle_categorical2(self,target:Feature):
        """Handle a categorical feature using ANOVA and Chi-Square."""

        # Apply One-Hot Encoding for categorical features
        encoder = OneHotEncoder(sparse_output=False)#, drop='first')
        encoded_feature = encoder.fit_transform(self.data.values.reshape(-1, 1))

        # Chi-Square Test
        contingency_table = pd.crosstab(self.data, target.data)
        chi2, p_chi, _, _ = chi2_contingency(contingency_table)

        # ANOVA for significance testing
        f_stat, p_anova = f_oneway(*[target.data[self.data == level] for level in self.data.unique()])

        return {'encoded': encoded_feature, 'chi2_p_value': p_chi, 'anova_p_value': p_anova}

    def handle_categorical(self, target):
        """Handle a categorical feature based on cardinality and importance."""
        # Check cardinality
        cardinality = self.data.nunique()

        if cardinality > 100:  # High cardinality
            print("High cardinality detected. Recommending target encoding.")
            # You would implement target encoding here.
        elif cardinality < 10:  # Low cardinality
            print("Low cardinality detected. Recommending one-hot encoding.")
            # encoder = OneHotEncoder(sparse=False, drop='first')
            # encoded_feature = encoder.fit_transform(self.data.values.reshape(-1, 1))
        else:
            print("Medium cardinality detected. Recommending frequency encoding.")

        # Chi-Square test for significance (for classification)
        contingency_table = pd.crosstab(self.data, target)
        chi2, p, dof, ex = chi2_contingency(contingency_table)
        if p < 0.05:
            print(f"Feature {self.data.name} is significant for the target.")
        else:
            print(f"Feature {self.data.name} is not significant for the target.")

        # return encoded_feature

    def recommendation(self, target):
        pass



def summarize_categorical_feature2(df, feature_name, target_name):
    """
    Generate a readable, rich CLI summary of a categorical feature in relation to the numerical target.
    """
    # Basic stats
    feature = df[feature_name]
    target = df[target_name]
    n_categories = feature.nunique()

    summary = f"Feature: {feature_name} (Categorical)\n"
    summary += "=" * len(summary) + "\n"

    # Cardinality check
    summary += f"Number of categories: {n_categories}\n"

    # Distribution of target per category
    category_target_means = df.groupby(feature_name)[target_name].mean()
    summary += "Target mean per category:\n"
    for cat, mean in category_target_means.items():
        summary += f"  {cat}: {mean:.4f}\n"

    # ANOVA or Kruskal-Wallis Test
    categories = df[feature_name].unique()
    target_by_category = [df[df[feature_name] == cat][target_name] for cat in categories]

    if n_categories > 2:
        kw_stat, kw_p_value = kruskal(*target_by_category)
        summary += f"\nKruskal-Wallis Test: H-statistic = {kw_stat:.4f}, p-value = {kw_p_value:.4f}\n"
    else:
        f_stat, p_value = f_oneway(*target_by_category)
        summary += f"\nANOVA Test: F-statistic = {f_stat:.4f}, p-value = {p_value:.4f}\n"

    # Check variance
    category_variances = df.groupby(feature_name)[target_name].var()
    summary += "\nVariance of target per category:\n"
    for cat, var in category_variances.items():
        summary += f"  {cat}: {var:.4f}\n"

    # Recommendations based on cardinality
    summary += "\nEncoding Recommendations:\n"

    # For low cardinality
    if n_categories <= 5:
        summary += "  - Use One-Hot Encoding as the number of categories is low.\n"

    # For medium cardinality (between 6 and 15)
    elif 6 <= n_categories <= 15:
        summary += "  - Consider Frequency Encoding since the number of categories is moderate.\n"

    # For high cardinality (> 15)
    else:
        target_variance = df[target_name].var()
        target_encoding_mean_diff = (df.groupby(feature_name)[target_name].mean() - df[target_name].mean()).abs()

        if target_encoding_mean_diff.mean() / target_variance > 0.1:
            summary += "  - Consider Target Encoding as it captures a significant difference in target values between categories.\n"
        else:
            summary += "  - Use Frequency Encoding as target encoding may overfit with high cardinality.\n"

    # Category grouping suggestion
    infrequent_categories = df[feature_name].value_counts()[df[feature_name].value_counts() < 5]
    if not infrequent_categories.empty:
        summary += "  - Group rare categories together, as some categories have very few observations.\n"

    # Outlier detection (per category)
    outliers = {}
    for cat, values in df.groupby(feature_name)[target_name]:
        q1, q3 = values.quantile(0.25), values.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers[cat] = values[(values < lower_bound) | (values > upper_bound)].count()

    summary += "\nOutliers detected per category:\n"
    for cat, outlier_count in outliers.items():
        summary += f"  {cat}: {outlier_count} outliers\n"

    # Recommendations based on outliers
    summary += "\nOutlier Recommendations:\n"
    if any(outliers.values()):
        summary += "  - Consider handling outliers, especially for categories with significant outliers.\n"
    else:
        summary += "  - No significant outliers detected in any category.\n"

    # Final conclusion
    summary += "\nConclusion:\n"
    summary += "  - Ensure encoding fits the cardinality and distribution of the categories.\n"
    summary += "  - Review category relationships to the target through statistical tests.\n"
    summary += "  - Handle outliers and group infrequent categories to stabilize model performance.\n"

    # Print the summary in a pretty, wrapped format
    # print(textwrap.fill(summary, width=80))
    print(summary)


import pandas as pd
import numpy as np
from scipy.stats import kruskal, spearmanr
import textwrap


def summarize_categorical_feature(df, feature_name, target_name, frequency_threshold=0.05):
    """
    Generate a rich CLI summary of a categorical feature in relation to a numerical target.
    This includes sorting by mean target, detecting rare categories, computing Kruskal-Wallis, etc.
    """
    feature = df[feature_name]
    target = df[target_name]

    # Number of entries and cardinality check
    category_counts = feature.value_counts()
    n_categories = feature.nunique()

    summary = f"Feature: {feature_name} (Categorical)\n"
    summary += "=" * len(summary) + "\n"
    summary += f"Number of categories: {n_categories}\n\n"

    # Target mean per category, number of entries, sorted by mean
    category_means = df.groupby(feature_name)[target_name].agg(['mean', 'count']).sort_values('mean')
    summary += "Target mean and number of entries per category (sorted by mean):\n"
    for cat, row in category_means.iterrows():
        summary += f"  {cat}: Mean = {row['mean']:.4f}, Count = {int(row['count'])}\n"

    # Detect and suggest combining rare categories
    total_entries = len(df)
    rare_categories = category_counts[category_counts / total_entries < frequency_threshold]
    if not rare_categories.empty:
        rare_mean_diff = abs(category_means.loc[rare_categories.index]['mean'] - category_means['mean'].mean())
        threshold_diff = rare_mean_diff.mean() / category_means['mean'].std()  # How close their means are
        summary += "\nRare category grouping suggestion:\n"

        similar_group = rare_categories.index[rare_mean_diff < threshold_diff]
        different_group = rare_categories.index[rare_mean_diff >= threshold_diff]

        if not similar_group.empty:
            summary += f"  - Group these rare categories together (similar means): {', '.join(similar_group)}\n"
        if not different_group.empty:
            summary += f"  - Group these rare categories together (different means): {', '.join(different_group)}\n"
    else:
        summary += "No rare categories detected.\n"

    # Frequency Encoding Suggestion based on correlation between category frequency and target
    category_frequencies = category_counts / total_entries
    freq_target_corr, p_value_freq_corr = spearmanr(category_frequencies, category_means['mean'])

    summary += "\nEncoding Recommendations:\n"
    if abs(freq_target_corr) > 0.3 and p_value_freq_corr < 0.05:
        summary += f"  - Consider using Frequency Encoding (frequency and target correlation = {freq_target_corr:.4f}, p-value = {p_value_freq_corr:.4f})\n"
    else:
        summary += "  - Frequency Encoding is not suggested. Consider One-Hot Encoding or Target Encoding.\n"

    # Kruskal-Wallis Test
    target_by_category = [df[df[feature_name] == cat][target_name] for cat in category_means.index]
    kw_stat, kw_p_value = kruskal(*target_by_category)
    summary += f"\nKruskal-Wallis Test:\n"
    summary += f"  H-statistic = {kw_stat:.4f}, p-value = {kw_p_value:.4f}\n"

    if kw_p_value < 0.05:
        summary += "  - The p-value is low, indicating significant differences in the target distribution between categories.\n"
    else:
        summary += "  - The p-value is high, suggesting no significant difference between categories.\n"

    # Variance Analysis (sorted)
    category_variances = df.groupby(feature_name)[target_name].var()
    variance_std = category_variances.std()
    variance_mean = category_variances.mean()

    summary += "\nVariance of target per category (sorted by variance):\n"
    for cat, var in category_variances.sort_values().items():
        variance_ratio = (var - variance_mean) / variance_std if variance_std > 0 else 0
        summary += f"  {cat}: Variance = {var:.4f} ({'high' if variance_ratio > 1 else 'low' if variance_ratio < -1 else 'moderate'})\n"

    summary += "\nVariance Interpretation:\n"
    if variance_std > 0:
        if max(category_variances) / min(category_variances) > 2:
            summary += "  - The variance between some categories is significantly different. Consider investigating these categories.\n"
        else:
            summary += "  - The variances are relatively similar between categories.\n"

    # Final conclusion
    summary += "\nConclusion:\n"
    summary += "  - Review category relationships to the target through statistical tests.\n"
    summary += "  - Handle outliers and group infrequent categories to stabilize model performance.\n"

    # Print the summary in a pretty, wrapped format
    print(summary)




