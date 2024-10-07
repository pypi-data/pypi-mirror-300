# Unit tests for data summary module
import unittest
from insightpy.core.analyzer.data_summary import DataSummary
import pandas as pd

class TestDataSummary(unittest.TestCase):
    def test_summary(self):
        data = pd.DataFrame({'col1': [1, 2, 3]})
        summary = DataSummary(data).generate()
        self.assertEqual(summary['mean']['col1'], 2)

if __name__ == "__main__":
    unittest.main()
