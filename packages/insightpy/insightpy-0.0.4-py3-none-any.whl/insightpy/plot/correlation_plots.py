# Correlation heatmap plotting
import matplotlib.pyplot as plt
import seaborn as sns

class CorrelationPlots:
    def __init__(self, data):
        self.data = data

    def plot(self):
        sns.heatmap(self.data.corr(), annot=True, cmap="coolwarm")
        plt.show()
