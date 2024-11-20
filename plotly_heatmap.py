import os
import pandas as pd
import plotly.express as px
from ruamel.yaml import YAML
from data_fetcher.data_fetcher import DataFetcher

def load_yaml(file_path):
    yaml = YAML(typ='safe')
    with open(file_path, 'r') as file:
        return yaml.load(file)

def fetch_and_process_data(fetcher, municipality, year, month):
    processed_data = fetcher.process_and_save_data(f"municipi='{municipality}'")
    processed_data['data'] = pd.to_datetime(processed_data['data'])
    return processed_data[(processed_data['data'].dt.year == year) & (processed_data['data'].dt.month == month)]

def initialize_accumulator(stations, pollutants):
    return pd.DataFrame(0, index=stations, columns=pollutants)

def update_accumulator(accumulator, processed_data, stations, pollutants, thresholds):
    for station in stations:
        for contaminant in pollutants:
            station_data = processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]
            if not station_data.empty:
                if contaminant in thresholds:
                    if station_data['value'].astype(float).quantile(q=0.99) > int(thresholds[contaminant]):
                        count_above_threshold = (station_data['value'].astype(float) > int(thresholds[contaminant])).sum()
                        accumulator.at[station, contaminant] = count_above_threshold
            else:
                accumulator.at[station, contaminant] = 'NaN'
    return accumulator

def plot_heatmap(accumulator, title):
    fig = px.imshow(accumulator)
    fig.update_layout(title=title)
    fig.show()

def main():
    yaml_file_path = 'WMO.yaml'
    thresholds = load_yaml(yaml_file_path)
    
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu", limit=2000)
    municipality = 'Barcelona'
    year = 2024
    month = 10
    
    processed_data = fetch_and_process_data(fetcher, municipality, year, month)
    
    stations = fetcher.list_available_options_with_filter("nom_estacio", f"municipi='{municipality}'")
    pollutants = thresholds.keys()
    
    accumulator = initialize_accumulator(stations, pollutants)
    accumulator = update_accumulator(accumulator, processed_data, stations, pollutants, thresholds)
    
    plot_heatmap(accumulator, f'Pollutant Threshold Exceedances in {municipality} Stations for {month}/{year}')

if __name__ == "__main__":
    main()
