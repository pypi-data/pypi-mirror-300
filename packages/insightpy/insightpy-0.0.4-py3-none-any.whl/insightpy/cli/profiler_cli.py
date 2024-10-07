# Initialize CLI
import click
from insightpy.core.data_summary import DataSummary
import pandas as pd
@click.command()
@click.argument('file')
def profile(file):
    data = pd.read_csv(file)
    summary = DataSummary(data).generate()
    print(summary)

if __name__ == "__main__":
    profile()
