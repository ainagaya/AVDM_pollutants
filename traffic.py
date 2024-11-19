from data_fetcher import DataFetcher
from graphics import accumulate_data
from graphics import plot_timeseries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#results_df = fetcher.fetch_data()
#results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
#Getting data from API 
fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=15000)

#Just bcn
processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

#We filter for NO2
N02=processed_data[processed_data['contaminant']=="NO2"]

# Now, obtain NO2 each day
FiltNO2= accumulate_data(processed_data,'Barcelona (Palau Reial)', 'NO2', 'D')

# Now i filter forjust january
jandata=FiltNO2[FiltNO2.index.to_series().dt.month == 1]

#Index near Palau Reial
indexe=[3,1,4,2,18,6,3,5,18,19,16,18,17,19,28,29]

# Getting data from csv file traffic
mice_csv=pd.read_csv('2024_01_Gener_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0)
# Dropping a column 
data=mice_csv.drop(columns=['estatPrevist'])

# Changing the date to a format that pandas can read
data['data']=pd.to_datetime(data['data'],format='%Y%m%d%H%M%S')

# Do a sum by day or hour
data2=data.loc[data.index.isin(indexe)].resample('D', on='data').sum()

# things to try to do for Hours
jandata=jandata.loc[jandata.index.isin(data2.index)]

# Eliminate rows that traffic info is 0
jandata2 = jandata.loc[(data2!=0).any(axis=1)]
# # Eliminate rows that traffic is 0
data2 = data2.loc[(data2!=0).any(axis=1)]

# # changing the value to make them comparable in a graph
data2=(data2['estatActual']-np.min(data2['estatActual']))/np.max(data2['estatActual'])
jandata2=(jandata2['value']-np.min(jandata2['value']))/np.max(jandata2['value'])


# Plotting the both list traffic and pollution january
plt.plot(data2,label='traffic')
plt.plot(jandata2,label='pollution of NO2')
plt.legend(loc='upper right')
plt.show()
