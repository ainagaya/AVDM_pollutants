#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

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

if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    #results_df = fetcher.fetch_data()
    #results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
    available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
    print(available_stations)