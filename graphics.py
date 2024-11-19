
import matplotlib.pyplot as plt
from data_fetcher.data_fetcher import DataFetcher
import pandas as pd

def plot_timeseries(data, title, ylabel, xlabel='Date', figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    data.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(f"{title}.png")
    plt.show()

def accumulate_data(data, station, contaminant, frequency):
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

    
    
