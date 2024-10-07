from insightpy.core.dataset.dataset import Dataset
from insightpy.core.feature.categorical_feature import summarize_categorical_feature, CategoricalFeature
from insightpy.core.profiler.profiler import Profiler
import pandas as pd
def analyze(data:pd.DataFrame,target_column:str):
    dataset = Dataset(data, target_column)
    profiler = Profiler(dataset)
    # profiler.recommend()
    for feature in profiler.dataset.features.values():
        if (isinstance(feature, CategoricalFeature)):
            summarize_categorical_feature(profiler.dataset.dataframe, feature.name, profiler.dataset.target_column)
        else:
            feature.summary(profiler.dataset.target)