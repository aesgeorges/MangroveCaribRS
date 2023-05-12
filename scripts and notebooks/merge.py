import os, glob, re, datetime
from osgeo import gdal
import numpy as np


from params import DOWNLOAD_DIR_HT, DOWNLOAD_DIR_TT

search_criteria = "*harmonized_clip_bandmath.TIF"

def paths_to_datetimeindex(list):
    """Converts a list of file paths to a list of datetime objects for given observations"""
    pattern = r'.*(\d{4}\d{2}\d{2}).*'
    new_list = []
    for item in list:
        time = re.search(pattern, item).group(1)
        time = datetime.datetime.strptime(time, '%Y%m%d').date()
        new_list.append(time)
    new_list = sorted(new_list)    
    return new_list

def find_files():
    ht_files = []
    tt_files = []

    # Accessing all the harmonized images in the download directories
    for dir,_,_ in os.walk(DOWNLOAD_DIR_HT):
        ht_files.extend(glob.glob(os.path.join(dir, search_criteria)))

    for dir,_,_ in os.walk(DOWNLOAD_DIR_TT):
        tt_files.extend(glob.glob(os.path.join(dir, search_criteria)))

    return ht_files, tt_files

def find_dates(ht_files, tt_files):
    """Finds the dates of the images in the download directories and pull the unique dates"""
    ht_dates = np.unique([i.strftime('%m-%d-%Y') for i in paths_to_datetimeindex(ht_files)])
    tt_dates = np.unique([i.strftime('%m-%d-%Y') for i in paths_to_datetimeindex(tt_files)])

    return ht_dates, tt_dates

def merge_observations(dates, files, dl_path):
    """Merges .tif files with same observation dates in a mosaic together"""
    for date in dates:
        samedate_files = []
        for file in files:
            filedate = paths_to_datetimeindex([file])[0].strftime('%m-%d-%Y')
            if filedate == date:
                samedate_files.append(file)
        path = dl_path + date + '.tif'
        mosaic = gdal.Warp(path, samedate_files, format='GTiff', srcNodata=0, dstNodata=0, multithread=True)
        mosaic = None

ht_files, tt_files = find_files()
ht_dates, tt_dates = find_dates(ht_files, tt_files)

merge_observations(ht_dates, ht_files, DOWNLOAD_DIR_HT)
#merge_observations(tt_dates, tt_files, DOWNLOAD_DIR_TT)


