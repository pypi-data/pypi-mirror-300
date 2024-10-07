# Profiler class for analyzing the dataset
from insightpy.core.dataset.dataset import Dataset


class Profiler:
    def __init__(self, dataset:Dataset):
        self.dataset = dataset


    def profile(self):
        """Run the main profiling routine."""
        for feature in self.dataset.features.values():
            print(f"Profiling feature: {feature.name}")
            print(feature.summary(self.dataset.target))
    def recommend(self):
        """Run the main profiling routine."""
        for feature in self.dataset.features.values():
            print(f"Profiling feature: {feature.name}")
            print(feature.recommendation(self.dataset.target))

if __name__ == '__main__':
    import pandas as pd
    df=pd.read_csv('../../cli/train.csv')
    dataset=Dataset(df,'SalePrice')
    profiler = Profiler(dataset)
    profiler.recommend()