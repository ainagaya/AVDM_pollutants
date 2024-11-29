# AVDM_pollutants

## What is it?

AVDM_pollutants is a study on traffic pollution before and after the Low Emission Zone (LEZ or ZBE in catalan) restrictions focused in Barcelona.

In this work we study the data that automatic enviromental stations provide each hour before and after the application of the LEZ in Barcelona. 

## Main features

- data_fetcher:
    - data_fetcher: to access the dataset with the API and do some data processing
    - graphics: to generate a possible figure
    - utils: functions for map and plotly generator
- Figures plotly: plotly code and figures 
- age_vehicle: code to generate figures related with age of vehicles and air pollutants
- compare_data_with_WMO
- example: code example of use of the dataset
- maps: map generator
- plotly_heatmap: code to generate plotly heatmaps
- traffic: code to generate figures related with traffic and air pollutants

## Acces to the dataset

To acces the dataset we use an API and connect with a token provided by the data portal.

The files to generate the maps can be downloaded executing the `download_shp.sh` script.

The files of other database are downloaded in CSV files.

## Requierements

The requirements in order to run the codes posted in this repository are especified in the file `requierements.txt`

After cloning the repository, create a virtual environment and execute `pip install .`. This will install the dependencies.

## Authors

- Armando Aguilar Campos @armandoaguilarcampos
- Joan Hernàndez Tey @JoanHTey
- Aina Gaya @ainagaya
- Diogo Correia @DiogoCorreia22
- Gonçalo Seoane @goncaloseoane
