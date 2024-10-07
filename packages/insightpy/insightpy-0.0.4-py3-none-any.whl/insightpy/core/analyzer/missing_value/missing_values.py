# Missing values analysis
class MissingValues:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        missing = self.data.isnull().sum()
        return missing
