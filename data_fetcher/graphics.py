
import matplotlib.pyplot as plt
from data_fetcher.data_fetcher import DataFetcher
import pandas as pd

"""
Contains functions to plot timeseries data
To be used as examples
"""


def plot_timeseries(data, title, ylabel, xlabel='Date', figsize=(10, 6)):
    """
    Plots a timeseries
    :param data: pd.DataFrame, timeseries data
    :param title: str, title of the plot
    :param ylabel: str, label for the y-axis
    :param xlabel: str, label for the x-axis
    :param figsize: tuple, size of the figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    data.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(f"{title}.png")
    plt.show()

def accumulate_data(data, station, contaminant, frequency):
    """
    Accumulates data for a given station and contaminant
    :param data: pd.DataFrame, data to be accumulated
    :param station: str, station name
    :param contaminant: str, contaminant name
    :param frequency: str, frequency for resampling
    :return: pd.DataFrame, resampled data
    """
    filtered_data = data[(data['nom_estacio'] == station) & (data['contaminant'] == contaminant)]
    numeric_data = filtered_data.drop(columns=['nom_estacio', 'contaminant'])

    numeric_data['value'] = pd.to_numeric(numeric_data['value'], errors='coerce')

    resampled = numeric_data.resample(frequency, on='data').sum()
    return resampled

if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

    resampled = accumulate_data(processed_data, 'Barcelona (Parc Vall Hebron)', 'CO', 'D')
    #resampled_daily = resampled.groupby(resampled.index.date).sum()
    plot_timeseries(resampled, "Daily CO Levels in Barcelona (Parc Vall Hebron)", "CO Levels")

    
    
