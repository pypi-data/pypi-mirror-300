import pandas as pd
# Base Feature class
class Feature:
    data:pd.Series
    def __init__(self, name: str, data):
        self.name = name
        self.data = data
        self.stats={}

    def summary(self,target):
        """Abstract method for generating a summary of the feature."""
        raise NotImplementedError

    def recommendation(self, target):
        raise NotImplementedError