from ruamel.yaml import YAML
import pandas as pd

import plotly.express as px
import math

import geopandas as gpd

import matplotlib.pyplot as plt 


def load_yaml(file_path):
    yaml = YAML(typ='safe')
    with open(file_path, 'r') as file:
        return yaml.load(file)
    
def initialize_accumulator(stations, pollutants):
    return pd.DataFrame(0, index=stations, columns=pollutants)

def update_accumulator(accumulator, processed_data, stations, pollutants, thresholds):
    for station in stations:
        for contaminant in pollutants:
            station_data = processed_data[(processed_data['nom_estacio'] == station) & (processed_data['contaminant'] == contaminant)]
            if not station_data.empty:
                if contaminant in thresholds:
                    if station_data['value'].astype(float).quantile(q=0.99) > int(thresholds[contaminant]):
                        count_above_threshold = (station_data['value'].astype(float) > int(thresholds[contaminant])).sum()
                        accumulator.at[station, contaminant] = count_above_threshold
            else:
                accumulator.at[station, contaminant] = 'NaN'
    return accumulator

def plot_heatmap(accumulator, title):
    fig = px.imshow(accumulator, color_continuous_scale='RdBu_r')
    fig.update_layout(title=title)
    fig.show()

def plot_heatmap_logscaled(accumulator, title):
    fig = px.imshow(accumulator.applymap(lambda x: 0 if x == 0 else ('NaN' if x == 'NaN' else math.log(x))), color_continuous_scale='RdBu_r')
    fig.update_layout(title=f'{title} in logscale')
    fig.show()

def plot_stations_in_map(station_coordinates):
    # Create a GeoDataFrame from the data
    if station_coordinates is not None:
        stations_df = gpd.GeoDataFrame(
            station_coordinates,
            geometry=gpd.points_from_xy(station_coordinates['longitud'], station_coordinates['latitud']),
            crs="EPSG:4326"  # WGS 84 coordinate system
        )
    else:
        raise ValueError("station_coordinates is None")

    # Load or create a base map (e.g., a world map)
    cat = gpd.read_file('shp_cat/divisions-administratives-v2r1-comarques-1000000-20240705.shp')

    stations_df = stations_df.to_crs(cat.crs)

    # Plot the map and add station points
    fig, ax = plt.subplots(figsize=(10, 10))
    cat.plot(ax=ax, color='lightgray', edgecolor='black')

    # Plot the stations
    stations_df.plot(ax=ax, color='blue', markersize=30)

    # Add labels for the stations (optional)
    #for x, y, label in zip(stations_df.geometry.x, stations_df.geometry.y, stations_df['nom_estacio']):
    #    ax.text(x, y, label, fontsize=9, ha='right')
    plt.title("Station locations")
    plt.show()

def plot_bubble_map(dataframe, station_coordinates, title, contaminant='NO2'):
    
    # Merge the dataframes on 'nom_estacio'
    print("dataframe: ", dataframe)
    print("station_coordinates: ", station_coordinates)

    # Split the columns, keep only the contaminant we want to plot
    dataframe = dataframe[contaminant]

    cat = gpd.read_file('shp_cat/divisions-administratives-v2r1-comarques-1000000-20240705.shp')

    # Create a GeoDataFrame from the data
    stations_df = gpd.GeoDataFrame(
        station_coordinates,
        geometry=gpd.points_from_xy(station_coordinates['longitud'], station_coordinates['latitud']),
        crs="EPSG:4326"  # WGS 84 coordinate system
    )

    stations_df = stations_df.to_crs(cat.crs)

    # Plot the map and add station points
    fig, ax = plt.subplots(figsize=(10, 10))
    cat.plot(ax=ax, color='lightgray', edgecolor='black')

    for station in stations_df['nom_estacio']:
        print("STATION: ", station)
        value = dataframe.get(station, 0)
        print("VALUE: ", value)
        # Plot the stations
        if value != 'NaN':
            stations_df[stations_df["nom_estacio"] == station].plot(ax=ax, color='blue', markersize=value, alpha=.2)

    plt.title(title)
    plt.show()
    plt.savefig(f'bubble_map_{title}.png')