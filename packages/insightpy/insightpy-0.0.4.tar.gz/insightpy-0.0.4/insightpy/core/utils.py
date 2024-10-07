from pandas import DataFrame
import pandas as pd

def is_numeric(df:DataFrame,column:str) -> bool:
    return df[column].dtype in ['int64', 'float64','bool']

def determine_feature_type(df, feature_name):
    """Determine if a feature is numerical or categorical."""
    if pd.api.types.is_numeric_dtype(df[feature_name]):
        return 'numerical'
    elif pd.api.types.is_categorical_dtype(df[feature_name]) or df[feature_name].nunique() < 10:
        return 'categorical'
    else:
        return 'unknown'

# # Usage:
# feature_type = determine_feature_type(df, 'feature_name')
# if feature_type == 'numerical':
#     handle_numerical(df['feature_name'], target)
# elif feature_type == 'categorical':
#     handle_categorical(df['feature_name'], target)
