
from data_fetcher import DataFetcher

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
#results_df = fetcher.fetch_data()
#results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
print(available_stations)

#codi_eoi
#nom_estacio
#data
#magnitud (Codi numèric que identifica el contaminant)
#contaminant
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

contaminants = fetcher.list_available_options_with_filter("contaminant", "municipi='Barcelona'") #UNION contaminant='NO2'")
print(contaminants)