
from data_fetcher import DataFetcher

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu")
#results_df = fetcher.fetch_data()
#results_filtered = fetcher.fetch_data_with_filter("municipi='Barcelona'")
available_stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
print(available_stations)