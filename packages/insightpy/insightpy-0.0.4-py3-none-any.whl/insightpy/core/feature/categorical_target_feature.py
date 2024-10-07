from insightpy.core.feature.base_target import Target
from insightpy.core.feature.categorical_feature import CategoricalFeature


class CategoricalTargetFeature(CategoricalFeature,Target):
    pass  # Can extend for target-specific behavior