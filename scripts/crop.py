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


# Using the site code, we find the images to be cropped (filepaths) and open the shapefile used to crop (clip_extent)
site_code = input('Enter the site code for which you want to crop the images (CCHT, CRTT, GPHT, etc.): ')
filepaths = DOWNLOAD_DIR_ROOT + site_code + '/*.tif'
shapepath  = '../'+ROOT_SHP + site_code + '_clip.shp'
clip_extent = gpd.read_file(shapepath)

# for each image in site to be cropped, crop and save in the cropped/site_code directory using same name as og file
for input in glob.glob(filepaths):
    date = paths_to_datetimeindex([input])
    export_path = DOWNLOAD_DIR_ROOT + 'cropped/' + site_code + '/' + str(date[0]) + '.tif'
    print("Cropping for " + site_code + '/' + str(date[0]))
    
    im = rxr.open_rasterio(input).squeeze()
    im = im.rio.clip(clip_extent.geometry.apply(mapping), clip_extent.crs)
    im.rio.to_raster(export_path, driver='GTiff', dstSRS='EPSG:32618')

