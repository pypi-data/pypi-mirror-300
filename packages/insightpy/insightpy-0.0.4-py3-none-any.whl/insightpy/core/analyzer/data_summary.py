# Summary statistics generation
class DataSummary:
    def __init__(self, data):
        self.data = data

    def generate(self):
        summary = {
            'mean': self.data.mean(),
            'median': self.data.median(),
            'std_dev': self.data.std()
        }
        return summary
