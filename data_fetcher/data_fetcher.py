#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
from datetime import datetime

class DataFetcher:
    """
    Class to fetch data from a Socrata dataset and process it
    """
    def __init__(self, domain, app_token, dataset_id, limit=2000):
        self.client = Socrata(domain, app_token)
        self.dataset_id = dataset_id
        self.limit = limit

    def fetch_data(self):
        """
        Fetches data from the dataset and returns it as a pandas DataFrame
        """
        results = self.client.get(self.dataset_id, limit=self.limit)
        return pd.DataFrame.from_records(results)
    
    def fetch_data_starting_from(self, start_date):
        """
        Fetches data from the dataset starting from a given date and returns it as a pandas DataFrame
        """
        results = self.client.get(self.dataset_id, where=f"data > '{start_date}'", limit=self.limit)
        return pd.DataFrame.from_records(results)

    def fetch_with_filter_and_data_and_process(self, start_date, filter,output_file='filtered_data_from.csv'):
        """
        Fetches data from the dataset starting from a given filter and filter again with date and returns it as a pandas DataFrame
        """
        results = self.client.get(self.dataset_id, where=filter, limit=self.limit)
        results_filtered = pd.DataFrame.from_records(results)
        results_filtered = results_filtered[results_filtered.data > start_date]
        results_filtered.fillna(0, inplace=True)

        new_table = pd.DataFrame(columns=results_filtered.columns)
        new_table = new_table.loc[:, ~new_table.columns.str.startswith('h')]

        melted_df = results_filtered.melt(id_vars=['data', 'nom_estacio', 'contaminant'], 
                                          value_vars=[f'h{i:02d}' for i in range(1, 25)], 
                                          var_name='hour', value_name='value')
        melted_df['hour'] = melted_df['hour'].str.extract('(\d+)').astype(int) - 1
        melted_df['data'] = pd.to_datetime(melted_df['data'])
        melted_df['data'] = melted_df.apply(lambda row: row['data'].replace(hour=row['hour']), axis=1)
        new_table = melted_df.drop(columns=['hour'])

        new_table = new_table.sort_values(by='data')

        new_table.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        return new_table
    
    def fetch_data_with_filter(self, filter):
        """
        Fetches data from the dataset with a filter and returns it as a pandas DataFrame
        """
        results = self.client.get(self.dataset_id, where=filter, limit=self.limit)
        return pd.DataFrame.from_records(results)
    
    def list_available_options(self, column_name):
        """
        Lists the available options for a given column in the dataset
        """
        results = self.client.get(self.dataset_id, select=column_name, limit=self.limit)
        return pd.DataFrame.from_records(results)[column_name].unique()
    
    def list_available_options_with_filter(self, column_name, filter):
        """
        Lists the available options for a given column in the dataset with a filter
        """
        results = self.client.get(self.dataset_id, select=column_name, where=filter, limit=self.limit)
        return pd.DataFrame.from_records(results)[column_name].unique()
    
    def get_coordinates(self, station):
        """
        Returns the coordinates of a station
        """
        # remove nan instances
        if not isinstance(station, str):
            return pd.DataFrame({})
        # Escape single quotes in the station name
        safe_station = station.replace("'", "''")
        
        results = self.client.get(self.dataset_id, where=f"nom_estacio='{safe_station}'", limit=1)
        return pd.DataFrame.from_records(results)[['nom_estacio', 'latitud', 'longitud']]


    def process_and_save_data(self, filter, output_file='filtered_data.csv'):
        """
        Fetches data from the dataset with a filter, processes it and saves it to a CSV file
        """

        # Retrieve the data, fill NaN values with 0 and remove the 'h' columns
        results_filtered = self.fetch_data_with_filter(filter)
        results_filtered.fillna(0, inplace=True)
        new_table = pd.DataFrame(columns=results_filtered.columns)
        new_table = new_table.loc[:, ~new_table.columns.str.startswith('h')]

        # Melt the DataFrame to have a row for each hour
        melted_df = results_filtered.melt(id_vars=['data', 'nom_estacio', 'contaminant'], 
                                          value_vars=[f'h{i:02d}' for i in range(1, 25)], 
                                          var_name='hour', value_name='value')
        # Extract the hour from the column name and subtract 1 to have the correct hour
        melted_df['hour'] = melted_df['hour'].str.extract('(\d+)').astype(int) - 1

        # Replace the date with the date and hour
        melted_df['data'] = pd.to_datetime(melted_df['data'])
        melted_df['data'] = melted_df.apply(lambda row: row['data'].replace(hour=row['hour']), axis=1)

        # Drop the hour column and sort the DataFrame by date
        new_table = melted_df.drop(columns=['hour'])
        new_table = new_table.sort_values(by='data')

        # Save the processed data to a CSV file
        new_table.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

        return new_table

    def process_and_save_data_no_filter(self, output_file='filtered_data.csv'):
        """
        Fetches data from the dataset without a filter, processes it and saves it to a CSV file
        """
        results_filtered = self.fetch_data()
        results_filtered.fillna(0, inplace=True)

        new_table = pd.DataFrame(columns=results_filtered.columns)
        new_table = new_table.loc[:, ~new_table.columns.str.startswith('h')]

        melted_df = results_filtered.melt(id_vars=['data', 'nom_estacio', 'contaminant'], 
                                          value_vars=[f'h{i:02d}' for i in range(1, 25)], 
                                          var_name='hour', value_name='value')
        melted_df['hour'] = melted_df['hour'].str.extract('(\d+)').astype(int) - 1
        melted_df['data'] = pd.to_datetime(melted_df['data'])
        melted_df['data'] = melted_df.apply(lambda row: row['data'].replace(hour=row['hour']), axis=1)
        new_table = melted_df.drop(columns=['hour'])

        new_table = new_table.sort_values(by='data')

        new_table.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        print("DEBUG: new_table", new_table)
        return new_table

    def fetch_and_process_data(self, municipality, year, month):
        """
        Fetches data from the dataset for a given municipality, year and month and processes it
        """
        processed_data = self.process_and_save_data(f"municipi='{municipality}'")
        processed_data['data'] = pd.to_datetime(processed_data['data'])
        if month == 'all':
            print(f"Data for {municipality} in {year} fetched and processed")
            return processed_data[processed_data['data'].dt.year == year]
        else:
            print(f"Data for {municipality} in {month}/{year} fetched and processed")
            print("DEBUG: processed data", processed_data)
            return processed_data[(processed_data['data'].dt.year == year) & (processed_data['data'].dt.month == int(month))]
        
    def fetch_and_process_data_no_filter(self, year, month):
        """
        Fetches data from the dataset for all municipalities, year and month and processes it
        """
        processed_data = self.process_and_save_data_no_filter()
        print("DEBUG: processed data", processed_data)
        processed_data['data'] = pd.to_datetime(processed_data['data'])
        if month == 'all':
            print(f"Data for all municipalities in {year} fetched and processed")
            print("DEBUG: processed data_year", processed_data['data'].dt.year)
            return processed_data[processed_data['data'].dt.year == year]
        else:
            print(f"Data for all municipalities in {month}/{year} fetched and processed")
            processed_data_filtered_yearly = processed_data[processed_data['data'].dt.year == year]
            print("DEBUG: processed data_year", processed_data_filtered_yearly)
            processed_data_filtered_monthly = processed_data_filtered_yearly[processed_data_filtered_yearly['data'].dt.month == int(month)]
            print("DEBUG: processed data_month", processed_data_filtered_monthly)
            return processed_data_filtered_monthly

        
    def get_station_coordinates(self, filter="None"):
        """
        Returns the coordinates of stations
        """
        if filter == "None":
            stations = self.list_available_options("nom_estacio")
        else:
            stations = self.list_available_options_with_filter("nom_estacio", filter)
        print("stations: ", stations)
        station_coordinates = pd.DataFrame({})
        for estacio in stations:
            station_coordinates = pd.concat([station_coordinates, self.get_coordinates(estacio)], ignore_index=True)
        return station_coordinates

if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    processed_data = fetcher.process_and_save_data("municipi='Barcelona'")
    print(processed_data)