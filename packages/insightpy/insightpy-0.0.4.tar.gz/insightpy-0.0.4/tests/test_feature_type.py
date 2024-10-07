import pytest
import pandas as pd
from insightpy.core.utils import determine_feature_type


def test_determine_feature_type():
    df = pd.DataFrame({
        'num_feature': [1.0, 2.5, 3.7, 4.1],
        'cat_feature': ['A', 'B', 'A', 'C'],
        'target': [1, 0, 1, 0]
    })

    assert determine_feature_type(df, 'num_feature') == 'numerical'
    assert determine_feature_type(df, 'cat_feature') == 'categorical'
    assert determine_feature_type(df, 'target') == 'numerical'

