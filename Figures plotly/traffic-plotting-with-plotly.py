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
jandata=FiltNO2[FiltNO2.index.to_series().dt.month.isin([1,2])]
#febdata=FiltNO2[FiltNO2.index.to_series().dt.month == 2]

#Index near Palau Reial
indexe=[3,1,4,2,18,6,3,5,18,19,16,18,17,19,28,29]

# Getting data from csv file traffic
mice_csv=pd.read_csv('2024_01_Gener_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0)
# Dropping a column 
jantraf=mice_csv.drop(columns=['estatPrevist'])

# Changing the date to a format that pandas can read
jantraf['data']=pd.to_datetime(jantraf['data'],format='%Y%m%d%H%M%S')

mice_csv=pd.read_csv('2024_01_Gener_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0)
# Dropping a column 
jantraf=mice_csv.drop(columns=['estatPrevist'])

# Changing the date to a format that pandas can read
jantraf['data']=pd.to_datetime(jantraf['data'],format='%Y%m%d%H%M%S')

mice_csv2=pd.read_csv('2024_02_Febrer_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0)
# Dropping a column 
febtraf=mice_csv2.drop(columns=['estatPrevist'])

# Changing the date to a format that pandas can read
febtraf['data']=pd.to_datetime(febtraf['data'],format='%Y%m%d%H%M%S')

c_df = pd.concat([jantraf, febtraf])
print(c_df)
# Do a sum by day or hour
cdf_sum=c_df.loc[c_df.index.isin(indexe)].resample('D', on='data').sum()

# # Same length same index
jandata=jandata.loc[jandata.index.isin(cdf_sum.index)]

# # Eliminate rows that traffic info is 0
jd_f = jandata.loc[(cdf_sum!=0).any(axis=1)]


# # # Eliminate rows that traffic is 0
jt_f = cdf_sum.loc[(cdf_sum!=0).any(axis=1)]

merged_df = jt_f.join(jd_f, how='inner')
# # changing the value to make them comparable in a graph
# data2=(data2['estatActual']-np.min(data2['estatActual']))/np.max(data2['estatActual'])
# jandata2=(jandata2['value']-np.min(jandata2['value']))/np.max(jandata2['value'])
#print(data2.iloc[:])

# Plotting the both list traffic and pollution january
#plt.plot(data2,label='traffic')
#plt.plot(jandata2,label='pollution of NO2')
# plt.plot(data2.iloc[:],jandata2.iloc[:],marker='o',linestyle=' ')
# plt.legend(loc='upper right')
# plt.show()

import plotly.express as px
df = px.data.iris()
fig = px.scatter(merged_df, x="estatActual", y="value")
fig.show()