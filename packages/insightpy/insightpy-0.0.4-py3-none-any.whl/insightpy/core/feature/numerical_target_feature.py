from insightpy.core.feature.base_target import Target
from insightpy.core.feature.numerical_feature import NumericalFeature


class NumericalTargetFeature(NumericalFeature,Target):
    pass  # Can extend for target-specific behavior