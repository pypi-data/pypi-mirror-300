import pytest
import pandas as pd

from insightpy.core.dataset.dataset import Dataset
from insightpy.core.profiler.profiler import Profiler
from insightpy.core.analyzer.interaction_analizer import InteractionAnalyzer

@pytest.fixture
def interaction_profiler()->Profiler:
    df = pd.DataFrame({
        'feature1': [1, 2, 3, 4],
        'feature2': [4, 3, 2, 1],
        'target': [1, 0, 1, 0]
    })
    dataset=Dataset(df,'target')
    profiler=Profiler(dataset)
    return profiler

def test_handle_interaction(interaction_profiler: Profiler):
    f = interaction_profiler.dataset.features
    interaction = InteractionAnalyzer.handle_interaction(f['feature1'], f['feature2'], interaction_profiler.dataset.target)

    # Check that interaction was calculated
    assert interaction.shape == (4,)
    assert (interaction == f['feature1'].data * f['feature2'].data).all()

