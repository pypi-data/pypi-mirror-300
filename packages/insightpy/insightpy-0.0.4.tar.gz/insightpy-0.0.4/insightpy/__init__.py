# sweetviz public interface
# -----------------------------------------------------------------------------------
try:
    from importlib.metadata import metadata # Python 3.8+
except ImportError:
    from importlib_metadata import metadata # Python 3.7

_metadata = metadata("insightpy")
__title__ = _metadata["name"]
__version__ = _metadata["version"]
__author__ = _metadata["Author-email"]
__license__ = "MIT"

# These are the main API functions
from insightpy.sv_public import analyze


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv('./insightpy/cli/train.csv')
    analyze(df, 'SalePrice')

