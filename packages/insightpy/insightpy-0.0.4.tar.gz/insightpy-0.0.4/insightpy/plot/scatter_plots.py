# Scatter plot visualizations
import matplotlib.pyplot as plt

class ScatterPlots:
    def __init__(self, data):
        self.data = data

    def plot(self, x, y):
        plt.scatter(self.data[x], self.data[y])
        plt.show()
