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
    
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu", limit=21000)
    municipality = 'all'
    year = 2024
    month = '10'
    #month = 'all'

    if month == 'all':
        last_data_needed = pd.to_datetime(f"{year}-01-01")
    else:
        last_data_needed = pd.to_datetime(f"{year}-{month}-01")

    first_data_needed = pd.to_datetime(f"{year}-12-31")

    print(f"Last data needed: {last_data_needed}")
    
    if municipality == 'all':
        processed_data = fetcher.fetch_and_process_data_no_filter(year, month)
        print(processed_data)
        stations = fetcher.list_available_options("nom_estacio")
        filter = "None"
    else:
        processed_data = fetcher.fetch_and_process_data(municipality, year, month)
        print("Processed data: ",  processed_data)
        stations = fetcher.list_available_options_with_filter("nom_estacio", f"municipi='{municipality}'")
        filter = f"municipi='{municipality}'"

    last_downloaded_data = pd.to_datetime(processed_data['data'].iloc[0])
    first_downloaded_data = pd.to_datetime(processed_data['data'].iloc[-1])

    print(f"Last downloaded data: {last_downloaded_data}")
    print(f"First downloaded data: {first_downloaded_data}")


    if last_downloaded_data > last_data_needed:
        raise ValueError("Data is outdated. You need to download more data.")
    
    total_hour_counts = processed_data.groupby('nom_estacio').size()
    print("total_hour_counts: ", total_hour_counts)
    
    pollutants = thresholds.keys()
    
    accumulator = initialize_accumulator(stations, pollutants)
    accumulator = update_accumulator(accumulator, processed_data, stations, pollutants, thresholds)

    # Remove stations with NaN values in the accumulator
    accumulator = accumulator.dropna()

    # Keep only the values for NO2, with the key 'NO2' in the column axis
    accumulator = accumulator['NO2']

    print("accumulator: ", accumulator)

    station_coordinates = fetcher.get_station_coordinates(filter=filter)

    print("station_coordinates: ", station_coordinates)

    plot_stations_in_map(station_coordinates)

    # normalize accumulator
    normalized_accumulator = accumulator.copy()
    for station in stations:
        print("station: ", station)
        try:
            print("accumulator.loc[station]: ", accumulator.loc[station])
        except:
            print("accumulator.loc[station]: ", 0)
        try:
            print("total_hour_counts.loc[station]: ", total_hour_counts.loc[station])
        except:
            print("total_hour_counts.loc[station]: ", 0)
        if accumulator.loc[station] != 'NaN':
            if total_hour_counts.loc[station] != 0 and total_hour_counts.loc[station] != 'NaN':
                try:
                    normalized_accumulator[station] = accumulator.loc[station] / total_hour_counts.loc[station]
                except:
                    normalized_accumulator[station] = 0
    print("normalized_accumulator: ", normalized_accumulator)

    #plot_bubble_map(accumulator, station_coordinates, f'NO2 hourly Threshold Exceedances in {municipality} Stations for {month}/{year}')

    plot_bubble_map(normalized_accumulator, station_coordinates, f'NO2 hourly Threshold Exceedances in {municipality} Stations for {month}/{year}')

if __name__ == "__main__":
    main()