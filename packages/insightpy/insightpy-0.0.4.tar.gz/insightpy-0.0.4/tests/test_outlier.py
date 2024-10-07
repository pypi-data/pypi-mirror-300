import pytest
import pandas as pd

from insightpy.core.dataset.dataset import Dataset
from insightpy.core.profiler.profiler import Profiler
from insightpy.core.analyzer.outlier_analyzer import OutlierAnalyzer

@pytest.fixture
def outlier_profiler()->Profiler:
    df = pd.DataFrame({
        'num_feature': [1.0, 2.5, 3.7, 4.1,4.2, 100.0],  # 100.0 is an outlier
        'cat_feature': ['A', 'B', 'A', 'C', 'B','B'],
        'target': [1, 0, 1, 0, 1,1]
    })
    dataset=Dataset(df,'target')
    profiler=Profiler(dataset)
    return profiler

def test_handle_outliers_and_scaling(outlier_profiler:Profiler)->None:

    scaled_feature = OutlierAnalyzer.handle_outliers_and_scaling(outlier_profiler.dataset.features['num_feature'])

    # Check if scaling output is correct
    assert len(scaled_feature) == len(outlier_profiler.dataset.dataframe)
    # Ensure outlier is capped (no value should be more extreme than the 1% quantile)
    assert max(scaled_feature) < 3.0

