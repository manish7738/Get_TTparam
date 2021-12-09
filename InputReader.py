# Import libraries & dependencies
import geopandas as gpd
import os


def InputReader(path, **layer):
    """This function can read files that is both in
    #Geojson
    #.gdb
    #shp
    #geopackage
    #csv (default ,)
    #excel"""

    name, extension = os.path.splitext(path)

    if ".shp" in str(path) or ".geojson" in str(path):
        try:
            solite_file = gpd.read_file(path)
            file_headers = solite_file.columns
            population = int(solite_file.shape[0])
            print("Population Size: ", population)

            return solite_file
        except:
            print("File could not be opened", extension)


    elif ".gdb" in str(path) or ".gpkg" in str(path):
        try:
            solite_file = gpd.read_file(path, layer=layer)  # SOLite_NetworkElements
            file_headers = solite_file.columns
            population = int(solite_file.shape[0])
            print("Population Size: ", population)
            return solite_file
        except:
            print("File could not be opened", extension)
