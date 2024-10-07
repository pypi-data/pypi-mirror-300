# Unit tests for missing values module
import unittest
from insightpy.core.analyzer.missing_value.missing_values import MissingValues
import pandas as pd

class TestMissingValues(unittest.TestCase):
    def test_missing_values(self):
        data = pd.DataFrame({'col1': [1, None, 3]})
        missing = MissingValues(data).analyze()
        self.assertEqual(missing['col1'], 1)

if __name__ == "__main__":
    unittest.main()
