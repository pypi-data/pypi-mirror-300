# Data loader utility
import pandas as pd

class DataLoader:
    def load_data(self, filepath):
        return pd.read_csv(filepath)
