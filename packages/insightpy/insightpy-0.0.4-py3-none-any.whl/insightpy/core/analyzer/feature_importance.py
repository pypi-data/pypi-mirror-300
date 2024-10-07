from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import pandas as pd


def feature_importance_with_rf(df, target, task_type='regression'):
    """Calculate feature importance using RandomForest."""
    if task_type == 'regression':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(df, target)
    importance = model.feature_importances_

    # Display feature importance
    importance_df = pd.DataFrame({'Feature': df.columns, 'Importance': importance})
    return importance_df.sort_values(by='Importance', ascending=False)


# # Usage:
# importance_df = feature_importance_with_rf(df.drop(columns='target'), df['target'])
# print(importance_df)
