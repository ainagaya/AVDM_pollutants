from ruamel.yaml import YAML

from data_fetcher.data_fetcher import DataFetcher
from data_fetcher.graphics import plot_timeseries, accumulate_data


import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

yaml = YAML(typ='safe')  # 'safe' is fine for loading

# Open the file and pass it to yaml.load()
with open('WMO.yaml', 'r') as file:
    data = yaml.load(file)

print(data)

fetcher = DataFetcher("analisi.transparenciacatalunya.cat", "9Hbf461pXC6Lin1yqkq414Fxi", "tasf-thgu", limit=100000)
processed_data = fetcher.process_and_save_data("municipi='Barcelona'")

stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
pollutants = fetcher.list_available_options_with_filter("contaminant", "municipi='Barcelona'")

accumulator = {station: 0 for station in stations}

print(accumulator)

#print(processed_data)

for station in stations:
    for contaminant in pollutants:
        if not processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)].empty:
            if contaminant in data:
                print("CONTAMINANT: ", contaminant)
                if processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]['value'].astype(float).quantile(q=0.99) > int(data[contaminant]):
                #if processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]['value'].astype(float) > int(data[contaminant]):
                    print("THRESHOLE EXCEEDED FOR: ", contaminant, " IN STATION: ", station)
                    accumulator[station] += 1



stations = fetcher.list_available_options_with_filter("nom_estacio", "municipi='Barcelona'")
station_coordinates = pd.DataFrame({})


for estacio in stations:
    station_coordinates = pd.concat([station_coordinates, fetcher.get_coordinates(estacio)], ignore_index=True)

# Create a GeoDataFrame from the data
stations_df = gpd.GeoDataFrame(
    station_coordinates,
    geometry=gpd.points_from_xy(station_coordinates['longitud'], station_coordinates['latitud']),
    crs="EPSG:4326"  # WGS 84 coordinate system
)

print(accumulator)

print(accumulator.values())

norm = sum(list((accumulator.values())))

accumulator = {station: accumulator[station]/norm for station in stations}

print(norm)

print(accumulator)

# Load or create a base map (e.g., a world map)
cat = gpd.read_file('shp_cat/divisions-administratives-v2r1-comarques-1000000-20240705.shp')

stations_df = stations_df.to_crs(cat.crs)

print(stations_df)

# Plot the map and add station points
fig, ax = plt.subplots(figsize=(10, 10))
cat.plot(ax=ax, color='lightgray', edgecolor='black')

for station in stations_df['nom_estacio']:
    print("STATION: ", station)
    value = accumulator.get(station, 0)
    print("VALUE: ", value)
    # Plot the stations
    stations_df[stations_df["nom_estacio"] == station].plot(ax=ax, color='red', markersize=value*100)

# Add labels for the stations (optional)
for x, y, label in zip(stations_df.geometry.x, stations_df.geometry.y, stations_df['nom_estacio']):
    ax.text(x, y, label, fontsize=9, ha='right')

# Set the limits for the plot to focus on the region near latitude 41 and longitude 2
ax.set_xlim(420000, 440000)
ax.set_ylim(4.575e6, 4.590e6)

plt.show()
