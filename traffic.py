
from data_fetcher.data_fetcher import DataFetcher
from data_fetcher.graphics import accumulate_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def safe_quantile(x, q=0.5, interpolation='higher'):
    non_zero_values = x[x > 0]
    return non_zero_values.quantile(q=q, interpolation=interpolation) if len(non_zero_values) > 0 else 0
def safe_mode(x):
    non_zero_values = x[x > 0]
    return non_zero_values.mode().iloc[0] if not non_zero_values.mode().empty else 0

def safe_min_nonzero(x):
    non_zero_values = x[x > 0]
    return non_zero_values.min() if len(non_zero_values) > 0 else 0
"""
In order for this code to work you need to have the Mandatory CSV files in the same folder as this code.

The files can be download in https://opendata-ajuntament.barcelona.cat/data/dataset/trams/resource/ec409c44-6a07-411d-8f53-efb5c1b7e989 
and in https://opendata-ajuntament.barcelona.cat/data/dataset/trams/resource/7ab9ef24-dd6d-40f4-a186-4563a491a81c
Also an aditional one is needed for the coords of the different stations:
https://opendata-ajuntament.barcelona.cat/data/ca/dataset/transit-relacio-trams/resource/c97072a3-3619-4547-84dd-f1999d2a3fec

With that and the requirements the code should run smoothly

"""




# Defining the parameters. This can change in order to obtain different pollutants and time lengths
pollu ='PM10'
T='H'
# To select the type of statistic : 1==max, 2==min, 3==mode, 4==median
Stat=4

#Getting data from API. this limits=15000 will change if you are running this code months later of november 2024. 
fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=15000)

# Now, obtain NO2 each day
processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

# Obtaining coordinates of traffic stations
estacions = fetcher.list_available_options_with_filter('nom_estacio',"municipi='Barcelona'and tipus_estacio='traffic'")
estacions2 = processed_data[processed_data['contaminant']==pollu]['nom_estacio'].unique()
estacions = list(set(estacions) & set(estacions2))
print(estacions)

# Obtaining units of the pollutant
unitat = fetcher.list_available_options_with_filter('unitats',f"contaminant='{pollu}'")

# Obtaining coordinates from the climate stations
coords=np.zeros([len(estacions),2])
for i in range(len(estacions)):
    a = fetcher.get_coordinates(estacions[i])
    coords[i]=np.array([float(a['latitud'][0]),float(a['longitud'][0])])
coords=np.array(coords)

# Maximum distance from a climate station to a traffic station
rad = 0.005642/10

# Obtaining the coordinates fro the traffic stations
mice_csv0=pd.read_csv('transit_relacio_trams_format_long.csv',
                         index_col=0,
                         header=0)
traf_estations = mice_csv0.reset_index()

# Obtaining the index of the traffic stations
indexes=[[],[]]
for i in range(1,len(traf_estations)):
    for j in range(len(estacions)):
        if rad**2>(float(traf_estations['Latitud'][i])-coords[j,0])**2+(float(traf_estations['Longitud'][i])-coords[j,1])**2 :
            indexes[j].append(float(traf_estations['Tram'][i]))

# Lets obtain the data from the climate stations
time = {'H':1,'D':24}
for i in range(len(estacions)):
    if i==0:
        FiltNO2 = accumulate_data(processed_data,estacions[i],f'{pollu}',T)
        FiltNO2['station'] = estacions[i]
        FiltNO2['value'] = FiltNO2['value']/time[T]
    else:
        FiltNO22 = accumulate_data(processed_data,estacions[i],f'{pollu}',T)
        FiltNO22['station'] = estacions[i]
        FiltNO22['value'] = FiltNO22['value']/time[T]
        if not (FiltNO22['value'] == 0).all():  # If not all values are zero
            FiltNO2 = pd.concat([FiltNO2, FiltNO22])
if (FiltNO2[FiltNO2['station'] == estacions[0]]['value'] == 0).all():
    FiltNO2 = FiltNO2[FiltNO2['station']==estacions[1]]
# If you are passed january 2025 you need to add a year filter for 2024 to get the same results
jandata=FiltNO2[FiltNO2.index.to_series().dt.month.isin([1,2])]

# Getting traffic data for months 1,2
#-----------------------------------------------------------------------------------
mice_csv=pd.read_csv('2024_01_Gener_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0)
jantraf=mice_csv.drop(columns=['estatPrevist'])
jantraf['data']=pd.to_datetime(jantraf['data'],format='%Y%m%d%H%M%S')
#-----------------------------------------------------------------------------------
mice_csv2=pd.read_csv('2024_02_Febrer_TRAMS_TRAMS.csv',
                         index_col=0,
                         header=0) 
febtraf=mice_csv2.drop(columns=['estatPrevist'])
febtraf['data']=pd.to_datetime(febtraf['data'],format='%Y%m%d%H%M%S')
#-----------------------------------------------------------------------------------
# Concat both months
c_df = pd.concat([jantraf, febtraf])


# Do a sum by day or hour
for i in range(len(estacions)):
    if i==0:
        cdf=c_df.loc[c_df.index.isin(indexes[i])]

        ind = list(set(indexes[i]))
        for i in ind:
            # Filter rows for specific index and check if 'estatActual' is always 0
            zero_rows = cdf[cdf.index == i]['estatActual']
            #print(f"Index {i}: Always zero = {(zero_rows == 0).all()}")
            if (zero_rows == 0).all()==True:
                cdf=cdf.drop(int(i))

        # Obtaining the selected statistical average
        if Stat==1: # Maximum
            cdf_0=cdf.resample(T, on='data')['estatActual'].max()
        if Stat==2: # Minimum
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(safe_min_nonzero)
        if Stat==3: # Mode
            #cdf_0=cdf.resample(T, on='data')['estatActual'].apply(lambda x: x[x > 0].mode().iloc[0] if not x[x > 0].mode().empty else None)
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(safe_mode)
        if Stat==4: # Median
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(safe_quantile)
            #cdf_0 = cdf.resample(T,on= 'data')['estatActual'].quantile(q=0.5,interpolation='higher')
            cdf_0 = cdf_0.to_frame(name='estatActual')
        # # Same length same index
        jandata_0=jandata.loc[jandata.index.isin(cdf_0.index)]

        merged_df = jandata_0.join(cdf_0, how='inner')
    else :
        cdf=c_df.loc[c_df.index.isin(indexes[i])]

        ind = list(set(indexes[i]))
        for i in ind:
            # Filter rows for specific index and check if 'estatActual' is always 0
            zero_rows = cdf[cdf.index == i]['estatActual']
            #print(f"Index {i}: Always zero = {(zero_rows == 0).all()}")
            if (zero_rows == 0).all()==True:
                cdf=cdf.drop(int(i))

# 
        if Stat==1: # Maximum
            cdf_0=cdf.resample(T, on='data')['estatActual'].max()
        if Stat==2: # Minimum
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(lambda x: x[x > 0].min() if any(x > 0) else None)
        if Stat==3: # Mode
            #cdf_0=cdf.resample(T, on='data')['estatActual'].apply(lambda x: x[x > 0].mode().iloc[0] if not x[x > 0].mode().empty else None)
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(safe_mode)
        if Stat==4: # Median
            #cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(lambda x: x[x > 0].quantile(q=0.5, interpolation='higher'))
            #cdf_0 = cdf.resample(T,on= 'data')['estatActual'].quantile(q=0.5,interpolation='higher')
            cdf_0 = cdf.resample(T, on='data')['estatActual'].apply(safe_quantile)
            cdf_0 = cdf_0.to_frame(name='estatActual')
        
        # # Same length same index
        jandata_0=jandata.loc[jandata.index.isin(cdf_0.index)]
        # Merge the different stations
        merged_df_0 = jandata_0.join(cdf_0, how='inner')
        merged_df = pd.concat([merged_df,merged_df_0])
 
merged_df=merged_df.reset_index()
merged_df = merged_df[merged_df['value']!=0]

# Change this value to obatin results for the different stations.
merged_df0 = merged_df[merged_df['station']==estacions[1]]

# Setting limits and max
Max = {'NO2':40,'PM2.5':25,'CO':10,'PM10':40}
Medium ={'NO2':20,'PM2.5':10,'CO':10,'PM10':20}
Minimum = {'NO2':10,'PM2.5':5,'CO':10,'PM10':15}

# trend line
coefficients = np.polyfit(merged_df0['estatActual'], merged_df0['value'], 1)
x=np.linspace(0,5,6)

trend = coefficients[0] * x + coefficients[1]

# Plot the results
plt.figure(figsize=(10,6))
sns.violinplot(x='estatActual', y='value', data=merged_df0)
plt.title(f'{pollu} level vs traffic density for hour during two months in {estacions[1]}',fontsize=14)
plt.ylim(bottom=0)
plt.xlabel('Traffic density',fontsize=14)
plt.ylabel(f'{pollu} level ({unitat[0]})',fontsize=14)

#Trend line
ymin, ymax = plt.ylim()
plt.plot(x,trend,linestyle='--',color='black',label='Trendline')

# This plots the colors bands showing the limits of the Pollution values
plt.axhspan(0, Minimum[pollu], color='green', alpha=0.3, label='WHO limits')
plt.axhspan(Minimum[pollu], Medium[pollu], color='yellowgreen', alpha=0.3, label='Legal future')
plt.axhspan(Medium[pollu], Max[pollu], color='yellow', alpha=0.3, label='Legal now')
plt.axhspan(Max[pollu],ymax,color='red', alpha=0.3, label='Ilegal')
plt.legend(loc='upper right',fontsize=14)
plt.show()


# fig = px.scatter(merged_df, x="estatActual", y="value")
# fig.show()