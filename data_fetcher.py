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

def add_column_month(df):
    df['month'] = pd.to_datetime(df['data']).dt.month
    return df

def add_column_day(df):
    df['day'] = pd.to_datetime(df['data']).dt.day
    return df

def add_column_year(df):
    df['year'] = pd.to_datetime(df['data']).dt.year
    return df

def get_monthly_average(df):
    return df.groupby('month').mean()

def get_daily_average(df):
    return df.groupby('day').mean()

def get_yearly_average(df):
    return df.groupby('year').mean()

if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    #results_df = fetcher.fetch_data()
    results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
    # Replace all NaN values with 0
    results_filtered.fillna(0, inplace=True)
    #available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
    #list_of_pollutants = fetcher.list_available_options_with_filter("contaminant", "municipi='Barcelona'")

    # Put each hour in a separate row, add the hour in the data column, delete the columns h01, h02, etc. 

    print(results_filtered)
    new_table = pd.DataFrame(columns=results_filtered.columns)
    new_table = new_table.loc[:, ~new_table.columns.str.startswith('h')]
    print(new_table)

    index = 0
    date_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_format_time = '%H:%M:%S'

    for date in results_filtered['data']:
        print(date)
        for i in range(0, 24):
            for station in results_filtered['nom_estacio'].unique():
                for contaminant in results_filtered['contaminant'].unique():
                    current_day = datetime.strptime(date, date_format).day
                    current_month = datetime.strptime(date, date_format).month
                    current_year = datetime.strptime(date, date_format).year
                    current_hour = i
                    date_with_hour = datetime(current_year, current_month, current_day, current_hour)
                    print("date_with_hour", date_with_hour)
                    new_row = results_filtered[results_filtered['data'] == date][results_filtered['nom_estacio'] == station][results_filtered['contaminant'] == contaminant]
                    new_row = new_row.loc[:, ~new_row.columns.str.startswith('h')]
                    new_row['data'] = date_with_hour
                    new_table = pd.concat([new_table, new_row], ignore_index=True)
                    index += 1

    print(new_table)  

    #results_filtered = results_filtered.melt(id_vars=['data', 'nom_estacio', 'contaminant'], var_name='hour', value_name='value')






    # columns_to_sum = [col for col in results_filtered.columns if col.startswith('h')]
    # results_filtered['daily_sum'] = 0
    # for col in columns_to_sum:
    #     results_filtered['daily_sum'] += results_filtered[col].astype(float)

    # results_filtered = add_column_day(results_filtered)
    # results_filtered["day"].apply(pd.to_numeric, errors='ignore')
    # results_filtered = add_column_month(results_filtered)
    # results_filtered["month"].apply(pd.to_numeric, errors='ignore')
    # results_filtered = add_column_year(results_filtered)
    # results_filtered["year"].apply(pd.to_numeric, errors='ignore')
    # results_filtered["daily_sum"].apply(pd.to_numeric, errors='ignore')

    
    # for station in results_filtered['nom_estacio'].unique():
    #     plt.figure(figsize=(10, 6))
    #     station_data = results_filtered[results_filtered['nom_estacio'] == station]
    #     # Distinguish per contaminant
    #     for contaminant in station_data['contaminant'].unique():
    #         station_data_contaminant = station_data[station_data['contaminant'] == contaminant]
    #         plt.plot(pd.to_datetime(station_data_contaminant['data']), station_data_contaminant['daily_sum'].astype(float), label=contaminant, marker=' ', linestyle='-')
    #     #plt.plot(pd.to_datetime(station_data['data']), station_data['daily_sum'].astype(float), label=station, marker='.', linestyle=' ')
    #     plt.xlabel('Date')
    #     plt.ylabel('daily_sum')
    #     plt.title(f'Daily sum vs Date for {station}')
    #     plt.legend()
    #     plt.show()

    # print(results_filtered)




    #monthly_average = get_monthly_average(results_filtered)
    #print(monthly_average)
    #daily_average = get_daily_average(results_filtered)
    #print(daily_average)
    #yearly_average = get_yearly_average(results_filtered)
    #print(yearly_average)
    #print(results_filtered["h01"].sum())
    #results_filtered['daily_sum'] = results_filtered[columns_to_sum].sum(axis=1)

    #print(results_filtered)
    
    #print(list_of_pollutants)
    #print(available_stations)