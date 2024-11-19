
from ruamel.yaml import YAML

import plotly.express as px

import os

from data_fetcher.data_fetcher import DataFetcher
import pandas as pd

yaml = YAML(typ='safe')  # 'safe' is fine for loading

# Open the file and pass it to yaml.load()
with open('WMO.yaml', 'r') as file:
    data = yaml.load(file)

print(data)

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu", limit=100000)
processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

last_data = processed_data.head(1)
print("last data: ", last_data)

# Filter data for October 2024
processed_data['data'] = pd.to_datetime(processed_data['data'])
october_2024_data = processed_data[(processed_data['data'].dt.year == 2024) & (processed_data['data'].dt.month == 10)]
processed_data = october_2024_data

#processed_data = fetcher.process_and_save_data_no_filter()

stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
pollutants = fetcher.list_available_options_with_filter("contaminant", "municipi='Barcelona'")

#stations = fetcher.list_available_options("nom_estacio")
#pollutants = fetcher.list_available_options("contaminant")

pollutants = data.keys()

accumulator = {station: 0 for station in stations}
accumulator = pd.DataFrame(0, index=stations, columns=pollutants)

print(accumulator)

#print(processed_data)

for station in stations:
    for contaminant in pollutants:
        if not processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)].empty:
            if contaminant in data:
                print("CONTAMINANT: ", contaminant)
                if processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]['value'].astype(float).quantile(q=0.99) > int(data[contaminant]):
                    count_above_threshold = (processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]['value'].astype(float) > int(data[contaminant])).sum()
                    accumulator.at[station, contaminant] = count_above_threshold
                #if processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]['value'].astype(float) > int(data[contaminant]):
                    print("THRESHOLE EXCEEDED FOR: ", contaminant, " IN STATION: ", station)
        else:
            print(f"Station {station} does not have data for {contaminant}")
            accumulator.at[station, contaminant] = 'NaN'

fig = px.imshow(accumulator)

fig.update_layout(title='Pollutant Threshold Exceedances in Barcelona Stations for October 2024')

fig.show()
