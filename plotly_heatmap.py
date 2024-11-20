import os
import pandas as pd
import plotly.express as px
from ruamel.yaml import YAML
from data_fetcher.data_fetcher import DataFetcher
from data_fetcher.utils import *
import math

def main():
    yaml_file_path = 'WMO.yaml'
    thresholds = load_yaml(yaml_file_path)
    
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu", limit=200000)
    municipality = 'Barcelona'
    year = 2016
    month = 'all'
    
    processed_data = fetcher.fetch_and_process_data(municipality, year, month)

    print(f"Last downloaded data: {processed_data['data'].head(1)}")
  
    stations = fetcher.list_available_options_with_filter("nom_estacio", f"municipi='{municipality}'")
    pollutants = thresholds.keys()
    
    accumulator = initialize_accumulator(stations, pollutants)
    accumulator = update_accumulator(accumulator, processed_data, stations, pollutants, thresholds)
    
    plot_heatmap(accumulator, f'Pollutant Threshold Exceedances in {municipality} Stations for {month}/{year}')

    plot_heatmap_logscaled(accumulator, f'Pollutant Threshold Exceedances in {municipality} Stations for {month}/{year}')

if __name__ == "__main__":
    main()
