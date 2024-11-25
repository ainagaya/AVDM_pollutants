
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
# Defining the parameters
pollu ='NO2'
T='H'
# To select the type of statistic : 1==max, 2==min, 3==mode, 4==median
Stat=4

#Getting data from API 
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
print(unitat)
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

        merged_df_0 = jandata_0.join(cdf_0, how='inner')
        merged_df = pd.concat([merged_df,merged_df_0])

merged_df=merged_df.reset_index()
merged_df = merged_df[merged_df['value']!=0]
print(merged_df)
merged_df0 = merged_df[merged_df['station']==estacions[0]]

# Setting limits and max
Max = {'NO2':40,'PM2.5':25,'CO':10,'PM10':40}
Medium ={'NO2':20,'PM2.5':10,'CO':10,'PM10':20}
Minimum = {'NO2':10,'PM2.5':5,'CO':10,'PM10':15}

# trend line
coefficients = np.polyfit(merged_df0['estatActual'], merged_df0['value'], 1)
x=np.linspace(0,5,6)

trend = coefficients[0] * x + coefficients[1]
print(trend)
# Plot the results
plt.figure(figsize=(10,6))
sns.violinplot(x='estatActual', y='value', data=merged_df0)
plt.title(f'{pollu} level vs Traffic Status for hour during January and February.')
plt.ylim(bottom=0)
plt.xlabel('Traffic Status')
plt.ylabel(f'{pollu} level ({unitat[0]})')
ymin, ymax = plt.ylim()
plt.plot(x,trend,linestyle='--',color='black',label='Trendline')

plt.axhspan(0, Minimum[pollu], color='green', alpha=0.3, label='WHO limits')
plt.axhspan(Minimum[pollu], Medium[pollu], color='yellowgreen', alpha=0.3, label='Legal future')
plt.axhspan(Medium[pollu], Max[pollu], color='yellow', alpha=0.3, label='Legal now')
plt.axhspan(Max[pollu],ymax,color='red', alpha=0.3, label='Ilegal')
plt.legend(loc='upper right')
plt.show()


# fig = px.scatter(merged_df, x="estatActual", y="value")
# fig.show()