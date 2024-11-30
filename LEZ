#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
from datetime import datetime

class DataFetcher:
    def _init_(self, domain, app_token, dataset_id, limit=1000):
        self.client = Socrata(domain, app_token)
        self.dataset_id = dataset_id
        self.limit = limit

    def fetch_data(self):
        """
        Fetches data from the dataset and returns it as a pandas DataFrame
        """
        results = self.client.get(self.dataset_id, limit=self.limit)
    
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
        # Escape single quotes in the station name
        safe_station = station.replace("'", "''")
        results = self.client.get(self.dataset_id, where=f"nom_estacio='{safe_station}'", limit=1)
        return pd.DataFrame.from_records(results)[['nom_estacio', 'latitud', 'longitud']]


    def process_and_save_data(self, filter, output_file='filtered_data.csv'):
        """
        Fetches data from the dataset with a filter, processes it and saves it to a CSV file
        """
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


if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
    processed_data = fetcher.process_and_save_data("municipi='Barcelona'")
    #processed_data = fetcher.process_and_save_data("magnitud=8")

    print(processed_data)


import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import matplotlib.dates as mpl_dates
from matplotlib.dates import DateFormatter

# y axis modification

# Define the specific y values you want to display
specific_ticks = [0, 10, 20, 30, 40, 50, 60, 70]
# Scale the y positions back to match the actual scale of your data (it was divided by 720)
scaled_ticks = [tick * 720 for tick in specific_ticks]
# Set the selected values positions on the y-axis
ax.set_yticks(scaled_ticks)


#divide by 720 2nd figure
def divide_by_ten(y, _):
    return f"{y/720:.1f}"

    # import the data
if __name__ == "__main__":
    fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")

#one for direct data and the other wiyh saved data with initial iterations/ limit set
    
    #processed_data = fetcher.process_and_save_data("municipi='Barcelona'", output_file = 'data_from_barcelona.csv') # you collect and save all the data in a file 
    processsed_data = pd.read_csv("data_from_barcelona.csv")
    
# filter by date what to plot
    filtered_df = processed_data.loc[(processed_data['data'] > '2009-01-01') & (processed_data['data'] < '2024-11-15')]
    print(filtered_df.head())



# filter by station, pollutant, sum of values interval
    resampled = accumulate_data(filtered_df, 'Barcelona (Sants)', 'NO2', 'm')
    
    
    
# the plot without trend lines added (2 plots generated) if i want 2
    #plot_timeseries(resampled/720, "Monthly NO2 Levels in Barcelona (Ciutadella)", "NO2 Levels (µg/m3)") 
    
#saves this plot in pc
    #output_path = r"C:\Users\gonca\Downloads\monthly_pm10_levels_barcelona_Ciutadella_2009.png"
    #plt.savefig(output_path, dpi=300)
    #print(f"Plot saved to: {output_path}")
    
# creating a new columns with date in datetime format (like the index)
    resampled['date'] = resampled.index
# converts to continuous values
    resampled['date'] = resampled['date'].apply(mpl_dates.date2num)


    
# Define the range for the subsets
    #subset_start_date = pd.to_datetime('2009-01-01')  # Start date for subset
    #subset_end_date = pd.to_datetime('2011-01-01')    # End date for subset

    #subset2_start_date = pd.to_datetime('2011-01-01') 
    #subset2_end_date = pd.to_datetime('2013-01-01')

    #subset3_start_date = pd.to_datetime('2013-01-01') 
    #subset3_end_date = pd.to_datetime('2015-01-01')

    #subset4_start_date = pd.to_datetime('2015-01-01') 
    #subset4_end_date = pd.to_datetime('2017-01-01')
    
    #subset5_start_date = pd.to_datetime('2017-01-01') 
    #subset5_end_date = pd.to_datetime('2020-03-01')
    
    #subset6_start_date = pd.to_datetime('2022-01-01') 
    #subset6_end_date = pd.to_datetime('2024-11-15')

    #subset7_start_date = pd.to_datetime('2022-01-01') 
    #subset7_end_date = pd.to_datetime('2024-11-15')

    
    
# Filter the data for the subset in the range created // creates variables a, b for trends (linear -> deg 1)
    #subset = resampled[(resampled.index >= subset_start_date) & (resampled.index <= subset_end_date)]
    #subset.tail()
    #b_subset, a_subset = np.polyfit(subset['date'], subset['value'], deg=1)

    #subset2 = resampled[(resampled.index >= subset2_start_date) & (resampled.index <= subset2_end_date)]
    #subset2.tail()
    #b_subset2, a_subset2 = np.polyfit(subset2['date'], subset2['value'], deg=1)

    #subset3 = resampled[(resampled.index >= subset3_start_date) & (resampled.index <= subset3_end_date)]
    #subset3.tail()
    #b_subset3, a_subset3 = np.polyfit(subset3['date'], subset3['value'], deg=1)  

    #subset4 = resampled[(resampled.index >= subset4_start_date) & (resampled.index <= subset4_end_date)]
    #subset4.tail()
    #b_subset4, a_subset4 = np.polyfit(subset4['date'], subset4['value'], deg=1)  

    #subset5 = resampled[(resampled.index >= subset5_start_date) & (resampled.index <= subset5_end_date)]
    #subset5.tail()
    #b_subset5, a_subset5 = np.polyfit(subset5['date'], subset5['value'], deg=1)  

    #subset6 = resampled[(resampled.index >= subset6_start_date) & (resampled.index <= subset6_end_date)]
    #subset6.tail()
    #b_subset6, a_subset6 = np.polyfit(subset6['date'], subset6['value'], deg=1)  

    #subset7 = resampled[(resampled.index >= subset7_start_date) & (resampled.index <= subset7_end_date)]
    #subset7.tail()
    #b_subset7, a_subset7 = np.polyfit(subset7['date'], subset7['value'], deg=1)  

    
    fig, ax = plt.subplots(figsize=(10, 6))

    
# plot original data  
    ax.plot(resampled.date, resampled.value,lw=1, label="Full Data - Monthly Sum")
    
# Plot regression lines (equation a + bx) / labels
    #ax.plot(subset.date, a_subset + b_subset * subset.date, color="red", lw=1, label="Trend 2009-2011")
    #ax.plot(subset2.date, a_subset2 + b_subset2 * subset2.date, color="green", lw=1, label="Trend 2011-2013")
    #ax.plot(subset3.date, a_subset3 + b_subset3 * subset3.date, color="blue", lw=1, label="Trend 2013-2015")
    #ax.plot(subset4.date, a_subset4 + b_subset4 * subset4.date, color="black", lw=1, label="Trend 2015-2017")
    #ax.plot(subset5.date, a_subset5 + b_subset5 * subset5.date, color="magenta", lw=1, label="Trend 2017-2020")
    #ax.plot(subset6.date, a_subset6 + b_subset6 * subset6.date, color="orange", lw=1, label="Trend after LEZ")
    #ax.plot(subset7.date, a_subset7 + b_subset7 * subset7.date, color="green", lw=1, label="Trend after LEZ")


# Manually set the limits for the X-axis (start and end dates)
    start_date = pd.to_datetime('2009-01-01')  # Start date
    end_date = pd.to_datetime('2024-11-15')    # End date
    ax.set_xlim(start_date, end_date)
    ax.set_xticks(pd.date_range(start=start_date, end=end_date, freq='12MS'))  # "MS" means Month Start
    plt.xticks(rotation=45, ha='right')
       
    ax.yaxis.set_major_formatter(FuncFormatter(divide_by_ten)) #applies the previous function for /720

# titles, labels, color...
    ax.set_yticks(scaled_ticks)
    ax.set_title("Monthly NO2 Levels in Barcelona (Sants)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Hourly Average of NO2 Levels (µg/m3)")
    ax.legend(loc="upper right")
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

# saves plot as png    
    plt.tight_layout()
    plt.savefig(f"Sant.png")
    plt.show()

# prints the a, b values
    #print(a_subset,b_subset)
    #print(a_subset2,b_subset2)
    #print(a_subset3,b_subset3)
    #print(a_subset4,b_subset4)
    #print(a_subset5,b_subset5)
    #print(a_subset6,b_subset6)


    #output_path_2 = r"C:\Users\gonca\Downloads\regression_line_2009.png"
    #plt.savefig(output_path_2, dpi=300)
    #print(f"Plot saved to: {output_path_2}")
