from data_fetcher.data_fetcher import DataFetcher
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_fetcher.graphics import plot_timeseries, accumulate_data # type: ignore
import seaborn as sns

# original columns of the dataset:
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
# # we get all avalible stations
# available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
# for station in available_stations:
#     available_contaminant = fetcher.list_available_options_with_filter("contaminant", "nom_estacio='%s'"%station)
#     print(station, available_contaminant, len(available_contaminant))
# pie plots of stations and contaminants
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
    # get the total value in Barcelona for each kind of antiquity
    antique_list = ['Tipus_Vehicles',antiguetat2020v3.columns[0]] #columns name
    num_cars_list = [type_car,antiguetat2020v3.iloc[1,0]] #values
    for i in range(len(val_anti)):
        df_antique = antiguetat2020v3[antiguetat2020v3.Antiguitat == val_anti[i]]
        antique_list.append(val_anti[i])
        num_cars_list.append(df_antique.sum(axis='rows', numeric_only = True)[antiguetat2020v3.columns[4]])
    df_result = pd.DataFrame([num_cars_list], columns=antique_list)
    return df_result

def num_vehi_by_age_T(file_name,type_car = 'Turismes'):
    """Function that extract the number of type_car by age in Barcelona and applies T. Also generates new columns"""
    antiguetat2020 = pd.read_csv(file_name)
    # drop no needed columns
    antiguetat2020v2 = antiguetat2020.drop(['Codi_Districte','Codi_Barri','Seccio_Censal','Nom_Barri'],axis=1)
    # list of vehicles we are not interested in
    ignored_type_car = np.delete(antiguetat2020v2.Tipus_Vehicles.unique(),np.where(antiguetat2020v2.Tipus_Vehicles.unique()==type_car)[0])
    # we drop all kinds of vehicles except the one we are interested in
    antiguetat2020v3 = antiguetat2020v2[~antiguetat2020v2.Tipus_Vehicles.isin(ignored_type_car)]
    # all possible ages of the vehicles
    val_anti = antiguetat2020v3.Antiguitat.unique()
    # get the total value in Barcelona for each kind of antiquity
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
    df_result = pd.DataFrame([[type_car]*n_col,[antiguetat2020v3.iloc[1,0]]*n_col,antique_list,num_cars_list,norm_num_cars_list], columns=range(n_col), index=['Vehicle','Year','Antiquity','Value','Perc_value_year'])
    return df_result.T

# Barcelona (Eixample) ['NO2' 'NO' 'O3' 'PM2.5' 'PM10' 'CO' 'SO2'] 7
# Barcelona (Ciutadella) ['NO2' 'O3' 'NO' 'NOX'] 4
# Barcelona (Observatori Fabra) ['PM10' 'NOX' 'NO2' 'O3' 'NO'] 5
# Barcelona (Parc Vall Hebron) ['NO' 'CO' 'NOX' 'O3' 'PM10' 'NO2' 'SO2' 'PM2.5'] 8
# Barcelona (Palau Reial) ['SO2' 'NO2' 'O3' 'NOX' 'NO' 'PM10' 'CO' 'PM2.5'] 8
# Barcelona (Poblenou) ['NOX' 'NO2' 'PM10' 'NO'] 4
# Barcelona (Gràcia - Sant Gervasi) ['NO' 'O3' 'NO2' 'SO2' 'NOX' 'PM10' 'CO'] 7
# Barcelona (Sants) ['NO' 'NO2' 'NOX'] 3

# extract data and filter by date for the first time
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
ax.ticklabel_format(axis='y',style='sci',scilimits = (0,0))
ax.legend(car_pollu)

def values_pollutant(data,station='Barcelona (Palau Reial)',pollutant='NO2',time='A'):
    """Function that extracts the values of a pollutant from the interval 2019-2023"""
    resampled = accumulate_data(data,station,pollutant, time)
    resampled = resampled.drop(index='2024-12-31')
    # i hate datatime index
    values_poll = [] #2019,2020,2021,2022,2023
    for i in range(resampled.shape[0]):
        values_poll.append(resampled.iat[i,0])
    values_poll_norm = values_poll/np.max(values_poll)
    return values_poll,values_poll_norm
    
# we get the values of the pollutant for the interval 2019-2023
values_no2, values_no2_norm = values_pollutant(processed_data)
values_co, values_co_norm = values_pollutant(processed_data,pollutant='CO')

# create the complete dataframe for interval 2019-2023 
vehicles = ['Turismes', 'Motos', 'Ciclomotors', 'Furgonetes', 'Camions', 'Altres vehicles']
new_vehicles = ['Touring cars', 'Motorcycles', 'Mopeds', 'Vans', 'Trucks', 'Other vehicles']
df_list = []
for v in vehicles:
    for i in np.arange(19,24):
        mini_df = num_vehi_by_age_T('num_vehicles_by_age/20%i_antiguitat_tipus_vehicle.csv'%i,type_car=v)
        # add value of pollutants
        # double_mini_df = pd.concat([mini_df]*2, ignore_index=True)
        # val_pollutants = [values_no2_norm[(2000+i)-2019]]*mini_df.shape[0]
        # val_pollutants.extend([values_co_norm[(2000+i)-2019]]*mini_df.shape[0])
        # name_pollutants = ['NO2']*mini_df.shape[0]
        # name_pollutants.extend(['CO']*mini_df.shape[0])
        # double_mini_df['Value_pollutant'] = val_pollutants
        # double_mini_df['Pollutant'] = name_pollutants
        mini_df['NO2'] = [values_no2_norm[int(mini_df.loc[0,'Year'])-2019]]*mini_df.shape[0]
        mini_df['CO'] = [values_co_norm[int(mini_df.loc[0,'Year'])-2019]]*mini_df.shape[0]
        mini_df = mini_df.replace({'Vehicle': v}, new_vehicles[vehicles.index(v)])
        df_list.append(mini_df)
year_age = pd.concat(df_list).reset_index()

# Figure 2
# plotting everything in stacked bars plots, we identifiy the most important vehicle and the most common age. 
years2 = [2023]
for y in np.arange(len(years2)):
    mod2_year_age = year_age[year_age['Year']==years2[y]]
    #Change the names of Antiquity column
    antiquity = ["Menys d'un any d'antiguitat", '1 any', '2 anys', '3 anys', '4 anys', '5 anys','6 anys', '7 anys', '8 anys', '9 anys', '10 anys', "D'11 a 20 anys",'Més de 20 anys', 'No consta']
    new_antiquity = ["<1", '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', ">10,<20 ",'>20', 'Unknown']
    for a in antiquity:
        mod2_year_age = mod2_year_age.replace({'Antiquity': a}, new_antiquity[antiquity.index(a)])
    # Group by 'Antiquity' and 'Vehicle' to sum the 'Value'
    grouped = mod2_year_age.groupby(['Antiquity', 'Vehicle']).agg({'Value': 'sum'}).reset_index()
    # Pivot the table so that 'Antiquity' is the index and each vehicle type is a column
    pivot_df = grouped.pivot(index='Antiquity', columns='Vehicle', values='Value')
    # Plot the stacked bar chart
    pivot_df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')
    plt.xlabel('Antiquity (years)')
    plt.ylabel('Number of units')
    plt.title('Vehicles by Age and Type in %s'%int(years2[y]))
    plt.xticks(rotation=45, ha='right')  
    plt.ticklabel_format(axis='y',style='sci', scilimits = (0,0))
    plt.legend(title="Vehicle", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()  

# Figure 3
# to plot diverse relations for this age, we first normalize to get better results.
mod_year_age = year_age[year_age['Antiquity']=='D\'11 a 20 anys'].reset_index()
# normalize the vehicle number
value_norm = []
for v in new_vehicles:
    small_df = mod_year_age[(mod_year_age.Vehicle == v)]
    for i in small_df.index:
        value_norm.append(small_df.Value[i]/small_df.Value.max())
mod_year_age['Norm_value'] = value_norm

def plot_fig2(df,pollutant='NO2'):
    """Function that plots a figure using a df and depending of the pollutant"""
    fig2 = sns.lmplot(data=df, x='Norm_value', y=pollutant, hue='Year', col='Vehicle', palette="flare")
    fig2.tight_layout(pad=2) 
    j = 0
    for ax in fig2.axes.flat:
        # we draw the line between initial and final points
        ini_coor = (df.loc[(j*5),'Norm_value'], df.loc[(j*5),pollutant])
        final_coor = (df.loc[(j*5+4),'Norm_value'], df.loc[(j*5+4),pollutant])
        ax.axline(ini_coor,final_coor, color='k', ls='--')
        ax.grid(True, axis='both', ls=':')
        ax.set(xlabel='Normalized number of vehicles', ylabel='Normalized NO2 value')
        j+=1

mod3_year_age = mod_year_age[(mod_year_age['Vehicle'] != 'Other vehicles')]
plot_fig2(mod3_year_age)
# plot_fig2(mod3_year_age,pollutant='CO')
plt.show()

# for pair figures
#  ['Touring cars', 'Motorcycles', 'Mopeds', 'Vans', 'Trucks', 'Other vehicles']
# no_car = [[0,1,2,3],[0,1,4,5],[2,3,4,5]]
# for i in no_car:
#     mod3a_year_age = mod_year_age[(mod_year_age['Vehicle'] != new_vehicles[i[0]])]
#     mod3b_year_age = mod3a_year_age[(mod3a_year_age['Vehicle'] != new_vehicles[i[1]])]
#     mod3c_year_age = mod3b_year_age[(mod3b_year_age['Vehicle'] != new_vehicles[i[2]])]
#     mod3d_year_age = mod3c_year_age[(mod3b_year_age['Vehicle'] != new_vehicles[i[3]])]
#     mod3d_year_age = (mod3d_year_age.drop(['level_0'],axis=1)).reset_index()
#     plot_fig2(mod3d_year_age)
#     # plot_fig2(mod_year_age,pollutant='CO')
#     plt.show()