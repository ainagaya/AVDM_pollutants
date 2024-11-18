
from data_fetcher import DataFetcher
import numpy as np
import matplotlib.pyplot as plt

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
#results_df = fetcher.fetch_data()
#results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
# available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
# print(available_stations) #'Barcelona (Parc Vall Hebron)' 'Barcelona (Observatori Fabra)'
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
available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
for station in available_stations:
    available_contaminant = fetcher.list_available_options_with_filter("contaminant", "nom_estacio='%s'"%station)
    print(station, available_contaminant, len(available_contaminant))
dfc = fetcher.process_and_save_data("municipi='Barcelona'")
# print(dfc.head)
# dfc['contaminant'].value_counts().plot.pie()
dfc['nom_estacio'].value_counts().plot.pie()
plt.show()