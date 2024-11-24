
from data_fetcher.data_fetcher import DataFetcher
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_fetcher.graphics import plot_timeseries, accumulate_data # type: ignore
import seaborn as sns

# columns database
#codi_eoi
#nom_estacio
#data
#magnitud (Codi numèric que identifica el contaminant)
#contaminant ('PM10' 'NO' 'PM2.5' 'NOX' 'O3' 'SO2' 'NO2' 'CO') #cars:NO2, CO, PM2.5
#unitats
#tipus_estacio
#area_urbana
#codi_ine
#municip
#codi_comarca
#nom comarca
#h01
#...
#h24
#altitud
#latitud
#longitud
#geocoded_column

# # which contaminants are detected by each station?
# available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
# for station in available_stations:
#     available_contaminant = fetcher.list_available_options_with_filter("contaminant", "nom_estacio='%s'"%station)
#     print(station, available_contaminant, len(available_contaminant))
# dfc = fetcher.process_and_save_data("municipi='Barcelona'")
# print(len(dfc))
# plt.figure('contaminants')
# dfc['contaminant'].value_counts().plot.pie()
# plt.figure('nom_estacio')
# dfc['nom_estacio'].value_counts().plot.pie()
# plt.show()

# antiguetat dels vehicles
def num_vehi_by_age(file_name,type_car = 'Turismes'):
    """Function that extract the number of type_car by age in Barcelona in shape (3,14)"""
    antiguetat2020 = pd.read_csv(file_name)
    # drop no needed columns
    antiguetat2020v2 = antiguetat2020.drop(['Codi_Districte','Codi_Barri','Seccio_Censal','Nom_Barri'],axis=1)
    # list of vehicles we are not interested in
    ignored_type_car = np.delete(antiguetat2020v2.Tipus_Vehicles.unique(),np.where(antiguetat2020v2.Tipus_Vehicles.unique()==type_car)[0])
    # we drop all kinds of vehicles except the one we are interested in
    antiguetat2020v3 = antiguetat2020v2[~antiguetat2020v2.Tipus_Vehicles.isin(ignored_type_car)]
    # all possible ages of the vehicles
    val_anti = antiguetat2020v3.Antiguitat.unique()
    # get the total value in Barcelona for each kind of antiquety
    antique_list = ['Tipus_Vehicles',antiguetat2020v3.columns[0]]
    num_cars_list = [type_car,antiguetat2020v3.iloc[1,0]]
    for i in range(len(val_anti)):
        df_antique = antiguetat2020v3[antiguetat2020v3.Antiguitat == val_anti[i]]
        antique_list.append(val_anti[i])
        num_cars_list.append(df_antique.sum(axis='rows', numeric_only = True)[antiguetat2020v3.columns[4]])
    df_result = pd.DataFrame([num_cars_list], columns=antique_list)
    return df_result

def num_vehi_by_age_T(file_name,type_car = 'Turismes'):
    """Function that extract the number of type_car by age in Barcelona in shape (14,3)"""
    antiguetat2020 = pd.read_csv(file_name)
    # drop no needed columns
    antiguetat2020v2 = antiguetat2020.drop(['Codi_Districte','Codi_Barri','Seccio_Censal','Nom_Barri'],axis=1)
    # list of vehicles we are not interested in
    ignored_type_car = np.delete(antiguetat2020v2.Tipus_Vehicles.unique(),np.where(antiguetat2020v2.Tipus_Vehicles.unique()==type_car)[0])
    # we drop all kinds of vehicles except the one we are interested in
    antiguetat2020v3 = antiguetat2020v2[~antiguetat2020v2.Tipus_Vehicles.isin(ignored_type_car)]
    # all possible ages of the vehicles
    val_anti = antiguetat2020v3.Antiguitat.unique()
    # get the total value in Barcelona for each kind of antiquety
    antique_list = []
    num_cars_list = []
    # pair each age with the corresponding value
    for i in range(len(val_anti)):
        df_antique = antiguetat2020v3[antiguetat2020v3.Antiguitat == val_anti[i]]
        antique_list.append(val_anti[i])
        num_cars_list.append(df_antique.sum(axis='rows', numeric_only = True)[antiguetat2020v3.columns[4]])
    # get the percentage values for year
    norm_num_cars_list = []
    for i in range(len(val_anti)):
        norm_num_cars_list.append(num_cars_list[i]/sum(num_cars_list))
    n_col = len(antique_list)
    df_result = pd.DataFrame([[type_car]*n_col,[antiguetat2020v3.iloc[1,0]]*n_col,antique_list,num_cars_list,norm_num_cars_list], columns=range(n_col), index=['Tipus_Vehicles','Any','Antiguitat','Valor','Perc_valor_any'])
    return df_result.T

# plot d '11 a 20 anys versus no2,co,pm2.5 in interval 2019-2023
# Barcelona (Eixample) ['NO2' 'NO' 'O3' 'PM2.5' 'PM10' 'CO' 'SO2'] 7
# Barcelona (Ciutadella) ['NO2' 'O3' 'NO' 'NOX'] 4
# Barcelona (Observatori Fabra) ['PM10' 'NOX' 'NO2' 'O3' 'NO'] 5
# Barcelona (Parc Vall Hebron) ['NO' 'CO' 'NOX' 'O3' 'PM10' 'NO2' 'SO2' 'PM2.5'] 8
# Barcelona (Palau Reial) ['SO2' 'NO2' 'O3' 'NOX' 'NO' 'PM10' 'CO' 'PM2.5'] 8
# Barcelona (Poblenou) ['NOX' 'NO2' 'PM10' 'NO'] 4
# Barcelona (Gràcia - Sant Gervasi) ['NO' 'O3' 'NO2' 'SO2' 'NOX' 'PM10' 'CO'] 7
# Barcelona (Sants) ['NO' 'NO2' 'NOX'] 3
# extract data and filter by date
# fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=200000)
# processed_data = fetcher.fetch_with_filter_and_data_and_process('2019-01-01T01:00:00.000',"municipi='Barcelona'")

# once data is extracted, use the .csv because is faster
processed_data = pd.read_csv('filtered_data_from.csv')
# return type of column data to datatime
processed_data['data'] = pd.to_datetime(processed_data['data'])
# print(processed_data['data'].min()) #2019-01-02 
# plot the corresponing car pollutants from interval 2019-2023 for a respective station
car_pollu = ['NO2','CO','PM2.5']
# Figure 1

fig, ax = plt.subplots()
for p in car_pollu:
    resampled = accumulate_data(processed_data,'Barcelona (Palau Reial)', p, 'A')
    resampled.plot(ax=ax)
ax.set_title('Detected car pollutants in Barcelona (Palau Reial) for interval 2019-2023')
ax.set_xlabel('Date')
ax.set_ylabel('Pollutants (ug/m^3)')
ax.legend(car_pollu)

def values_pollutant(data,station='Barcelona (Palau Reial)',pollutant='NO2',time='A'):
    """Function that extracts the values of a pollutant from the interval 2019-2023"""
    resampled = accumulate_data(data,station,pollutant, time)
    resampled = resampled.drop(index='2024-12-31')
    # i hate datatime index
    values_poll = [] #2019,2020,2021,2022,2023
    for i in range(resampled.shape[0]):
        values_poll.append(resampled.iat[i,0])
    return values_poll
    
# we get the values of the pollutant for the interval 2019-2023
values_no2 = values_pollutant(processed_data)
values_co = values_pollutant(processed_data,pollutant='CO')

# create the complete dataframe for interval 2019-2023 
vehicles = ['Turismes', 'Motos', 'Ciclomotors', 'Furgonetes', 'Camions', 'Altres vehicles']
df_list = []
for v in vehicles:
    for i in np.arange(19,24):
        mini_df = num_vehi_by_age_T('num_vehicles_by_age/20%i_antiguitat_tipus_vehicle.csv'%i,type_car=v)
        # add value of pollutants
        mini_df['NO2'] = [values_no2[int(mini_df.loc[0,'Any'])-2019]]*mini_df.shape[0]
        mini_df['CO'] = [values_co[int(mini_df.loc[0,'Any'])-2019]]*mini_df.shape[0]
        df_list.append(mini_df)
year_age = pd.concat(df_list).reset_index()

# Figure 2
mod_year_age = year_age[year_age['Antiguitat']=='D\'11 a 20 anys'].reset_index()
# normalize the vehicle number
valor_norm = []
for v in vehicles:
    small_df = mod_year_age[(mod_year_age.Tipus_Vehicles == v)]
    for i in small_df.index:
        valor_norm.append(small_df.Valor[i]/small_df.Valor.max())
mod_year_age['Valor_norm'] = valor_norm

def plot_fig2(df,pollutant='NO2'):
    """Function that plots a figure using a df and depending of the pollutant"""
    fig2 = sns.lmplot(data=df, x='Valor_norm', y=pollutant, hue='Any', col='Tipus_Vehicles')
    j = 0
    for ax in fig2.axes.flat:
        ini_coor = (df.loc[(j*5),'Valor_norm'], df.loc[(j*5),pollutant])
        final_coor = (df.loc[(j*5+4),'Valor_norm'], df.loc[(j*5+4),pollutant])
        ax.axline(ini_coor,final_coor, color='k', ls='-')
        ax.grid(True, axis='both', ls=':')
        j+=1


plot_fig2(mod_year_age)
# plot_fig2(mod_year_age,pollutant='CO')
# plt.show()

# Bar Chart, Line Chart, Heatmap
# plottin everything, we identifiy the mist important vehicle and the most common age. we can fixate in the plot.
# to plot diverse relations for this age, we first normalize to get better results.

# Figure 3
mod2_year_age = year_age[year_age['Any']==2019]
# Group by 'Antiguitat' and 'Tipus_Vehicles' to sum the 'Valor'
grouped = mod2_year_age.groupby(['Antiguitat', 'Tipus_Vehicles']).agg({'Valor': 'sum'}).reset_index()
# Pivot the table so that 'Antiguitat' is the index and each vehicle type is a column
pivot_df = grouped.pivot(index='Antiguitat', columns='Tipus_Vehicles', values='Valor')
# Plot the stacked bar chart
pivot_df.plot( kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')

plt.xlabel('Antiguitat')
plt.ylabel('Valor')
plt.title('Stacked Bar Chart: Valor of Vehicles by Age and Type')
plt.xticks(rotation=45, ha='right')  
plt.legend(title="Tipus de Vehicles", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  
plt.show()



