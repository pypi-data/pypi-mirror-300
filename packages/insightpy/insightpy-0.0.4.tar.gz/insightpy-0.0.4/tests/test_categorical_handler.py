import pytest
import pandas as pd

from insightpy.core.dataset.dataset import Dataset
from insightpy.core.profiler.profiler import Profiler



@pytest.fixture
def profiler()->Profiler:
    df = pd.DataFrame({
        'num_feature': [1.0, 2.5, 3.7, 4.1, 5.6],
        'cat_feature': ['A', 'B', 'A', 'C', 'B'],
        'target': [1, 0, 1, 0, 1]
    })
    dataset=Dataset(df,'target')
    profiler=Profiler(dataset)
    return profiler


def test_handle_numerical(profiler:Profiler)->None:
    scaled_feature=profiler.dataset.features['num_feature'].handle_numerical(profiler.dataset.target)

    # Check if the output is scaled correctly
    assert scaled_feature.shape == (5, 1)
    assert abs(scaled_feature.mean()) < 1e-5  # Check if scaled feature has zero mean
    assert abs(scaled_feature.std() - 1) < 1e-5  # Check if scaled feature has unit variance

def test_handle_categorical(profiler:Profiler)->None:
    result=profiler.dataset.features['cat_feature'].handle_categorical(profiler.dataset.target)


def test_handle_categorical2(profiler:Profiler)->None:
    result=profiler.dataset.features['cat_feature'].handle_categorical2(profiler.dataset.target)
    # result = handle_categorical2(df['cat_feature'], df['target'])

    # Check if encoding works correctly
    assert result['encoded'].shape == (5, 3)  # One-Hot for 3 categories -> 2 encoded columns
    # Chi-Square significance test
    assert result['chi2_p_value'] <= 1.0
    # ANOVA p-value test
    assert result['anova_p_value'] <= 1.0

