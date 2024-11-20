
from data_fetcher.data_fetcher import DataFetcher
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=3000)
results_df = fetcher.fetch_data()
results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
print(available_stations) 
# available_stations: 'Barcelona (Parc Vall Hebron)' 'Barcelona (Observatori Fabra)'
# 'Barcelona (Palau Reial)' 'Barcelona (Eixample)' 'Barcelona (Ciutadella)'
# 'Barcelona (Gràcia - Sant Gervasi)' 'Barcelona (Poblenou)''Barcelona (Sants)'

# columns of the dataset:
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

dfc= fetcher.fetch_data_with_filter("municipi='Barcelona'")
print(dfc.head(3))
print(dfc.loc[:,'h01'])

# which contaminants are detected by each sector?
# Barcelona (Eixample) ['NO2' 'NO' 'O3' 'PM2.5' 'PM10' 'CO' 'SO2'] 7
# Barcelona (Ciutadella) ['NO2' 'O3' 'NO' 'NOX'] 4
# Barcelona (Observatori Fabra) ['PM10' 'NOX' 'NO2' 'O3' 'NO'] 5
# Barcelona (Parc Vall Hebron) ['NO' 'CO' 'NOX' 'O3' 'PM10' 'NO2' 'SO2' 'PM2.5'] 8
# Barcelona (Palau Reial) ['SO2' 'NO2' 'O3' 'NOX' 'NO' 'PM10' 'CO' 'PM2.5'] 8
# Barcelona (Poblenou) ['NOX' 'NO2' 'PM10' 'NO'] 4
# Barcelona (Gràcia - Sant Gervasi) ['NO' 'O3' 'NO2' 'SO2' 'NOX' 'PM10' 'CO'] 7
# Barcelona (Sants) ['NO' 'NO2' 'NOX'] 3
available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
for station in available_stations:
    available_contaminant = fetcher.list_available_options_with_filter("contaminant", "nom_estacio='%s'"%station)
    print(station, available_contaminant, len(available_contaminant))
dfc = fetcher.process_and_save_data("municipi='Barcelona'")
print(len(dfc))
plt.figure('contaminants')
dfc['contaminant'].value_counts().plot.pie()
plt.figure('nom_estacio')
dfc['nom_estacio'].value_counts().plot.pie()
plt.show()

# antiguetat dels vehicles
def num_vehi_by_age(file_name,type_car = 'Turismes'):
    """Function that extract the number of type_car by age in Barcelona"""
    antiguetat2020 = pd.read_csv(file_name)
    # drop no needed columns
    antiguetat2020v2 = antiguetat2020.drop(['Codi_Districte','Codi_Barri','Seccio_Censal','Nom_Barri'],axis=1)
    # list of vehicles we are not interested in
    ignored_type_car = np.delete(antiguetat2020v2.Tipus_Vehicles.unique(),np.where(antiguetat2020v2.Tipus_Vehicles.unique()==type_car)[0])
    # we drop all kinds of vehicles except the one we are interested in
    antiguetat2020v3 = antiguetat2020v2[~antiguetat2020v2.Tipus_Vehicles.isin(ignored_type_car)]
    # all possible ages of the vehicles
    val_anti = antiguetat2020v3.Antiguitat.unique()
    print(antiguetat2020v3.columns)
    # get the total value in Barcelona for each kind of antiquety
    years = np.ones((len(val_anti),1))*antiguetat2020v3.loc[1,antiguetat2020v3.columns[0]]
    df_result= pd.DataFrame(years, columns=[antiguetat2020v3.columns[0]])
    antique_list = []
    num_cars_list = []
    for i in range(len(val_anti)):
        df_antique = antiguetat2020v3[antiguetat2020v3.Antiguitat == val_anti[i]]
        antique_list.append(val_anti[i])
        num_cars_list.append(df_antique.sum(axis='rows', numeric_only = True)[antiguetat2020v3.columns[4]])
    df_result[antiguetat2020v3.columns[3]] = antique_list
    df_result[antiguetat2020v3.columns[4]] = num_cars_list

    return df_result
