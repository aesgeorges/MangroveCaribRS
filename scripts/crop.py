"""This script crops an existing merged image to a new AOI provided by a
shapefile. This is to clean up the images used for classification and analysis
to avoid excessive false positives from non-mangrove areas in the classification process."""

print('Welcome to crop tool!')

import geopandas as gpd
import rioxarray as rxr
import os, glob, re, datetime, math
from shapely.geometry import mapping

import sys
sys.path.append('/global/home/users/alexandregeorges/Chapter1/')

from codebase.params import *
from codebase.utils import *


# Using the site and shape code, we find the images to be cropped (filepaths) and open the shapefile used to crop (clip_extent)
site_code = input('Enter the site codename for which you want to crop the images (CCHT, CRTT, GPHT, etc.): ')
shape_code = input('Enter the codename for the shapefile used (GPHT, GPHT_landward, GPHT_seaward, etc.): ')
subregion = input('Is this a subregion crop? (Y/True) or a cleaning crop (N/False): ')

filepaths = DOWNLOAD_DIR_ROOT + site_code + '/*.tif'
shapepath  = '../'+ROOT_SHP + shape_code + '.shp'
clip_extent = gpd.read_file(shapepath)

# for each image in site to be cropped, crop and save in the cropped/site_code directory using same name as og file
for input in glob.glob(filepaths):
    date = [i.strftime('%m-%d-%Y') for i in paths_to_datetimeindex([input])]
    
    if subregion in ['True', 'Y', 'Yes']:
        export_path = DOWNLOAD_DIR_ROOT + shape_code + '/' + str(date[0]) + '.tif'
    elif subregion in ['False', 'N', 'No']:
        export_path = DOWNLOAD_DIR_ROOT + 'cropped/' + site_code + '/' + str(date[0]) + '.tif'
    else:
        print("Invalid input. Please enter 'Y/True' or 'N/False'.")
        break
    
    print("Cropping for " + site_code + '/' + str(date[0]))
    
    im = rxr.open_rasterio(input).squeeze()
    im = im.rio.clip(clip_extent.geometry.apply(mapping), clip_extent.crs)
    im.rio.to_raster(export_path, driver='GTiff', dstSRS='EPSG:32618')
    
### Known issues in this script
""" 10-16-23: rasterio will not create a non-existing folder in a given directory. You need to either create the non-existing folders yourself before running the code or create the folder on the fly using os.makedirs or similar functions (see https://discuss.python.org/t/allow-open-to-create-non-existent-directories-in-write-mode/16165)
    Why is this still here?: Me being stubborn, chose to create folders before running script, but this may not be user friendly at scale.
"""