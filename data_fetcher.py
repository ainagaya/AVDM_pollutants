#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
from datetime import datetime

class DataFetcher:
    def __init__(self, domain, app_token, dataset_id, limit=2000):
        self.client = Socrata(domain, app_token)
        self.dataset_id = dataset_id
        self.limit = limit

    def fetch_data(self):
        results = self.client.get(self.dataset_id, limit=self.limit)
        return pd.DataFrame.from_records(results)
    
    def fetch_data_with_filter(self, filter, limit=2000):
        results = self.client.get(self.dataset_id, where=filter, limit=limit)
        return pd.DataFrame.from_records(results)
    
    def list_available_options(self, column_name, limit=2000):
        results = self.client.get(self.dataset_id, select=column_name, limit=limit)
        return pd.DataFrame.from_records(results)[column_name].unique()
    
    def list_available_options_with_filter(self, column_name, filter, limit=2000):
        results = self.client.get(self.dataset_id, select=column_name, where=filter, limit=limit)
        return pd.DataFrame.from_records(results)[column_name].unique()

    def process_and_save_data(self, filter, output_file='filtered_data.csv'):
        results_filtered = self.fetch_data_with_filter(filter)
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

def get_monthly_average(df):
    return df.groupby('month').mean()

def get_daily_average(df):
    return df.groupby('day').mean()

def get_yearly_average(df):
    return df.groupby('year').mean()

if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    processed_data = fetcher.process_and_save_data("municipi='Barcelona'")
    print(processed_data)