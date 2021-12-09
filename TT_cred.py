########################################################################################
# ---------------This script helps to get TomTom related details, like MN-R server,  ###
# MN-R schema, Country code and epsg code for any given input polygon -------------- ###
# -----------------------------------------------------------------------------------###
# -----------------------------------------------------------------------------------###
# By Manish Panchal ####################################################################
########################################################################################

# Import libraries / dependencies
import psycopg2
import geopandas as gpd
import requests
from InputReader import InputReader

# File path
path = 'C:\\Manish\\Python\\PyCharmProject\\Get_cred\\Colombo_AOI.shp'

solite = InputReader(path)


def get_param():
    # Process AOI input file
    solite['centre'] = solite.geometry.centroid
    pt = solite.centre[0].wkt

    # Connect global spatial file from db
    conn = psycopg2.connect(host='weu-gdt-centerline-db.postgres.database.azure.com',
                            user='grip_ro@weu-gdt-centerline-db',
                            password='grip_ro',
                            database='gripdb')

    # Intersect query within input point & global data
    sql = "select * FROM grip.grip_global as gbl " \
          "where ST_Intersects(gbl.geom, ST_GeomFromText('" + pt + "',4326))"

    # Create dataframe from intersection
    gbl = gpd.read_postgis(sql, conn)
    utm = gbl['utm_zone'].iloc[0]

    # EPSG API
    url = "https://apps.epsg.org/api/v1/Conversion/"
    zone = {'keywords': utm}  # Adding UTM zone as parameter to EPSG API

    r = requests.get(url=url, params=zone)
    data = r.json()

    # Get all required details
    country = gbl['name'].iloc[0]
    ccode = gbl['isocode'].iloc[0]
    server = gbl['mnr_server'].iloc[0]
    schema = gbl['mnr_schema'].iloc[0]
    epsg = data['Results'][0]['Code']

    return country, ccode, server, schema, epsg


print('', get_param()[0], ' \n', get_param()[1], '\n', get_param()[2], '\n', get_param()[3], '\n', get_param()[4])
