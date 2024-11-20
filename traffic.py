
from data_fetcher.data_fetcher import DataFetcher
from data_fetcher.graphics import accumulate_data
from data_fetcher.graphics import plot_timeseries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def filter_data_and_sum(data,tipusestacio,pollutant,frequency):
    filtered_data = data[(data['tipus_estacio'] == traffic) & (data['contaminant'] == contaminant)]
    numeric_data = filtered_data.drop(columns=['nom_estacio', 'contaminant','tipus estacio'])

    numeric_data['value'] = pd.to_numeric(numeric_data['value'], errors='coerce')

    resampled = numeric_data.resample(frequency, on='data').sum()
    return resampled


#Getting data from API 
fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=15000)

#Just bcn

bcn_data = fetcher.fetch_data_with_filter("municipi='Barcelona'")
traff_data = bcn_data[bcn_data['tipus_estacio']=='traffic']

# Obtaining coordinates of traffic stations
estacions = fetcher.list_available_options_with_filter('nom_estacio',"municipi='Barcelona'and tipus_estacio='traffic'")
coords=[[],[]]
for i in range(len(estacions)):
    a = fetcher.get_coordinates(estacions[i])
    coords[i]=np.array([float(a['latitud'][0]),float(a['longitud'][0])])

rad = 0.005642


mice_csv0=pd.read_csv('transit_relacio_trams_format_long.csv',
                         index_col=0,
                         header=0)

traf_estations = mice_csv0.reset_index()
coords=np.array(coords)
indexes=[]

for i in range(1,len(traf_estations)):
    if rad**2>(float(traf_estations['Latitud'][i])-coords[0,0])**2+(float(traf_estations['Longitud'][i])-coords[0,1])**2 or rad**2>(float(traf_estations['Latitud'][i]-coords[1,0])**2+float(traf_estations['Longitud'][i]-coords[1,1])**2):
        indexes.append(float(traf_estations['Tram'][i]))



#We filter for NO2
#N02=processed_data[processed_data['contaminant']=="NO2"]

# Now, obtain NO2 each day
processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

FiltNO2 = accumulate_data(processed_data,estacions[0],'NO2','D')
FiltNO22 = accumulate_data(processed_data,estacions[1],'NO2','D')
FiltNO2['value'] = FiltNO2['value'] + FiltNO22['value']


# Now i filter forjust january
jandata=FiltNO2[FiltNO2.index.to_series().dt.month.isin([1,2])]


# Getting data from csv file traffic
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

# Do a sum by day or hour
#plt.hist(c_df.loc[c_df.index.isin(indexes)]['estatActual'][:])
cdf=c_df.loc[c_df.index.isin(indexes)]
print(cdf[cdf['data'].dt.hour.isin([12,15])])
plt.hist(cdf[cdf['data'].dt.hour.isin([12,15])]['estatActual'][:])
plt.show()
#cdf_sum=c_df.loc[c_df.index.isin(indexes)].resample('D', on='data').sum()


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


import plotly.express as px
df = px.data.iris()
fig = px.scatter(merged_df, x="estatActual", y="value")
fig.show()