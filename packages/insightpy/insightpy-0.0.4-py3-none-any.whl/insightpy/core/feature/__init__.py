from .base_feature import Feature
from .base_target import Target
from .categorical_target_feature import CategoricalTargetFeature
from .numerical_feature import NumericalFeature
from .categorical_feature import CategoricalFeature
from .numerical_target_feature import NumericalTargetFeature
from .. import utils


def get_target( dataframe, target_column) -> Target:
    if utils.is_numeric(dataframe, target_column):
        return NumericalTargetFeature(target_column, dataframe[target_column])
    else:
        return CategoricalTargetFeature(target_column, dataframe[target_column])