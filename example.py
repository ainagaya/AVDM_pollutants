
# from data_fetcher import DataFetcher
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu",limit=3000)
#results_df = fetcher.fetch_data()
#results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
# available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
# print(available_stations) #available_stations: 'Barcelona (Parc Vall Hebron)' 'Barcelona (Observatori Fabra)'
# 'Barcelona (Palau Reial)' 'Barcelona (Eixample)' 'Barcelona (Ciutadella)'
# 'Barcelona (Gràcia - Sant Gervasi)' 'Barcelona (Poblenou)''Barcelona (Sants)'

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

# dfc= fetcher.fetch_data_with_filter("municipi='Barcelona'")
# print(table_contaminants.head)
# print(dfc.loc[:,'h01'])

# which contaminants are detected by each sector?
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
antiguetat2020 = pd.read_csv('2020_antiguitat_tipus_vehicle.csv')
# drop no needed columns
antiguetat2020v2 = antiguetat2020.drop(['Codi_Districte','Codi_Barri','Seccio_Censal','Nom_Barri'],axis=1)
# we drop all kinds of vehicles except turisms
antiguetat2020v3 = antiguetat2020v2[~antiguetat2020v2.Tipus_Vehicles.isin(antiguetat2020v2.Tipus_Vehicles.unique()[1:])]
print(len(antiguetat2020v3))
val_anti = antiguetat2020v3.Antiguitat.unique()
print(val_anti)
# get the total value in Barcelona for each kind of antiquety
years = np.ones((len(val_anti),1))*antiguetat2020v3.loc[1,'Any']
df_result= pd.DataFrame(years, columns=['Any'])
antique_list = []
num_cars_list = []
for i in range(len(val_anti)):
    df_antique = antiguetat2020v3[antiguetat2020v3.Antiguitat == val_anti[i]]
    antique_list.append(val_anti[i])
    num_cars_list.append(df_antique.sum(axis='rows', numeric_only = True)['Nombre'])
df_result['Antiguetat'] = antique_list
df_result['Nombre'] = num_cars_list
print(df_result)
