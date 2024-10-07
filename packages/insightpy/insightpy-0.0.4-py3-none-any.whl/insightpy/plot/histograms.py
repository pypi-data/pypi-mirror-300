# Histograms plotting
import matplotlib.pyplot as plt

class Histograms:
    def __init__(self, data):
        self.data = data

    def plot(self):
        self.data.hist()
        plt.show()
