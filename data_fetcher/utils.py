from ruamel.yaml import YAML
import pandas as pd

import plotly.express as px
import math

import geopandas as gpd

import matplotlib.pyplot as plt 


def load_yaml(file_path):
    """
    Load a YAML file and return its contents.
    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: Contents of the YAML file.
    """
    yaml = YAML(typ='safe')
    with open(file_path, 'r') as file:
        return yaml.load(file)
    
def initialize_accumulator(stations, pollutants):
    """
    Initialize an accumulator DataFrame with zeros.
    Args:
        stations (list): List of station names.
        pollutants (list): List of pollutant names.
    Returns:
        pd.DataFrame: DataFrame initialized with zeros.
    """
    return pd.DataFrame(0, index=stations, columns=pollutants)

def update_accumulator(accumulator, processed_data, stations, pollutants, thresholds):
    """
    Update the accumulator DataFrame with counts of threshold exceedances.
    Args:
        accumulator (pd.DataFrame): DataFrame to be updated.
        processed_data (pd.DataFrame): DataFrame containing processed data.
        stations (list): List of station names.
        pollutants (list): List of pollutant names.
        thresholds (dict): Dictionary of thresholds for each pollutant.
    Returns:
        pd.DataFrame: Updated accumulator DataFrame.
    """
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
    """
    Plot a heatmap of the accumulator DataFrame.
    Args:
        accumulator (pd.DataFrame): DataFrame to be plotted.
        title (str): Title of the heatmap.
    """
    fig = px.imshow(accumulator, color_continuous_scale='RdBu_r')
    fig.update_layout(title=title)
    fig.show()

def plot_heatmap_logscaled(accumulator, title):
    """
    Plot a log-scaled heatmap of the accumulator DataFrame.
    Args:
        accumulator (pd.DataFrame): DataFrame to be plotted.
        title (str): Title of the heatmap.
    """
    fig = px.imshow(accumulator.applymap(lambda x: 0 if x == 0 else ('NaN' if x == 'NaN' else math.log(x))), color_continuous_scale='RdBu_r')
    fig.update_layout(title=f'{title} in logscale')
    fig.show()

def plot_stations_in_map(station_coordinates):
    """
    Plot the locations of stations on a map.
    Args:
        station_coordinates (pd.DataFrame): DataFrame containing station coordinates with columns 'longitud' and 'latitud'.
    Raises:
        ValueError: If station_coordinates is None.
    """
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
    ax.axis('off')

    # Plot the stations
    stations_df.plot(ax=ax, color='blue', markersize=30)

    # Add labels for the stations (optional)
    #for x, y, label in zip(stations_df.geometry.x, stations_df.geometry.y, stations_df['nom_estacio']):
    #    ax.text(x, y, label, fontsize=9, ha='right')
    plt.title("Station locations")
    plt.show()

def plot_bubble_map(dataframe, station_coordinates, title, contaminant='NO2'):
    """
    Plot a bubble map showing the exceedances of a specific contaminant.
    Args:
        dataframe (pd.DataFrame): DataFrame containing exceedance data.
        station_coordinates (pd.DataFrame): DataFrame containing station coordinates with columns 'longitud' and 'latitud'.
        title (str): Title of the bubble map.
        contaminant (str): Name of the contaminant to plot. Default is 'NO2'.
    """
    
    # Merge the dataframes on 'nom_estacio'
    print("dataframe: ", dataframe)
    print("station_coordinates: ", station_coordinates)

    # Split the columns, keep only the contaminant we want to plot
    try:
        dataframe = dataframe[contaminant]
    except KeyError:
        dataframe = dataframe

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
    ax.axis('off')
    cat.plot(ax=ax, color='lightgray', edgecolor='black')

    # Maximum value of the dataframe
    max_value = dataframe.apply(pd.to_numeric, errors='coerce').max() * 24

    print("max_value: ", max_value)
        

    for station in stations_df['nom_estacio']:
        print("STATION: ", station)
        value = dataframe.get(station, 0)
        print("VALUE: ", value)
        # Plot the stations
        if value != 'NaN':
            percentage = value * 100
            print(station, percentage)
            color = plt.cm.magma(value*24 / max_value)
            stations_df[stations_df["nom_estacio"] == station].plot(ax=ax, markersize=percentage*10, alpha=.4, color=color)

    # Add a legend with circle sizes, the value indicates how many times the threshold was exceeded
    for value in [1, 5, 10, 20]:
        plt.scatter([], [], c='blue', alpha=0.2, s=value*10, label=str(value))
    # Add a color bar with the colors used to represent the threshold exceedances
    sm = plt.cm.ScalarMappable(cmap=plt.cm.magma, norm=plt.Normalize(vmin=0, vmax=max_value))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Average threshold exceedances per day')
    plt.legend(title='% of threshold exceedances', loc='upper right', frameon=False)
    plt.title(title)

    # Add a small square showing Barcelona
    inset_ax = fig.add_axes([0.4, 0.1, 0.2, 0.2])
    cat.plot(ax=inset_ax, color='lightgray', edgecolor='black')
    for station in stations_df['nom_estacio']:
        print("STATION: ", station)
        value = dataframe.get(station, 0)
        print("VALUE: ", value)
        # Plot the stations
        if value != 'NaN':
            percentage = value * 100
            print(station, percentage)
            color = plt.cm.magma(value * 24 / max_value)
            stations_df[stations_df["nom_estacio"] == station].plot(ax=inset_ax, markersize=percentage*10, alpha=.4, color=color)
    inset_ax.axis('off')
    inset_ax.set_xlim(410000, 440000)
    inset_ax.set_ylim(4.57e6, 4.595e6)
    inset_ax.set_title('Barcelona')


    plt.show()

    # remove '/' from the title
    title = title.replace('/', '')
    plt.savefig(f'bubble_map_{title}.png')