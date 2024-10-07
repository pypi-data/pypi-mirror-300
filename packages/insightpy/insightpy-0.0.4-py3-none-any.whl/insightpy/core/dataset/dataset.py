from insightpy.core import utils
from insightpy.core.feature.base_target import Target
from insightpy.core.feature.categorical_feature import CategoricalFeature
from insightpy.core.feature.numerical_feature import NumericalFeature
import pandas as pd
import insightpy.core.feature as feature

class Dataset:
    def __init__(self, dataframe:pd.DataFrame,target_column:str='target'):
        self.dataframe = dataframe
        self.target=feature.get_target(dataframe,target_column)

        self.features = self._extract_features()

    @property
    def target_column(self):
        """
        :return: name of the target column
        """
        return self.target.name

    def _extract_features(self):
        """Dynamically create features based on the data type of each column."""
        features = {}
        for column in self.dataframe.columns:
            if column==self.target_column:
                pass
            else:
                if self.is_numeric(column):
                    features[column]=NumericalFeature(column, self.dataframe[column])
                else:
                    features[column]=CategoricalFeature(column, self.dataframe[column])
        return features

    def is_numeric(self, column:str):
        return utils.is_numeric(self.dataframe,column)

    def get_feature(self, name):
        """Retrieve a feature by name."""
        for feature in self.features:
            if feature.name == name:
                return feature
        return None