print('Welcome to merge tool!')

import os, glob, re, datetime, math
import scipy.stats as stats
from numpy import testing
import rioxarray as rxr
from osgeo import gdal
import numpy as np

import sys
sys.path.append('/global/home/users/alexandregeorges/[Chapter1] MangroveCaribRS/')

from codebase.params import DOWNLOAD_DIR_ROOT

# Search criteria for observation files to be mosaic merged based on Planet naming convention.
search_criteria = "*_clip_bandmath.tif" #"*harmonized_clip_bandmath.TIF"

def paths_to_datetimeindex(list):
    """Converts a list of file paths to a list of datetime objects for given observations"""
    pattern = r'.*(\d{4}-\d{2}-\d{2}).*'
    pattern_1 = r'.*(\d{4}\d{2}\d{2}).*'
    new_list = []
    for item in list:
        # Try different date formats, ReOrtho and PSScene have different naming conventions
        try:
            time = re.search(pattern, item).group(1)
            time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
        except:
            time = re.search(pattern_1, item).group(1)
            time = datetime.datetime.strptime(time, '%Y%m%d').date()
        new_list.append(time)
    new_list = sorted(new_list)    
    return new_list

def find_files(DOWNLOAD_DIR):
    """Return list of observation files present in download folder."""
    print('finding files to merge...')
    _files = []

    # Accessing all the harmonized images in the download directories
    for dir,_,_ in os.walk(DOWNLOAD_DIR):
        _files.extend(glob.glob(os.path.join(dir, search_criteria)))

    return _files

def find_dates(_files):
    """Finds the dates of the images in the download directories and pull the unique dates"""
    _dates = np.unique([i.strftime('%m-%d-%Y') for i in paths_to_datetimeindex(_files)])
    #tt_dates = np.unique([i.strftime('%m-%d-%Y') for i in paths_to_datetimeindex(tt_files)])
    
    print(str(len(_dates)) + ' observations were found...')
        
    return _dates

def quality_control(files):
    """
    Check whether merged .tif files covers the whole area of interest-if yes, proceed. if not, delete the merged file.
    
    Counts the amount of NaNs in each merged file, determining how much 
    uncovered area there is in the merged file. I take the mode of the NaN counts as a baseline
    for what is considered 'full coverage'. If an image is not within 10% tolerance of that
    baseline, it is considered not fully covered. I use tolerance as NaNs sometimes show up in
    covered areas.
    """

    files_to_check = [rxr.open_rasterio(f) for f in files]
    nan_counts = [f[-1].isnull().sum().values for f in files_to_check]
    baseline = stats.mode(nan_counts, keepdims=True).mode

    print('QC: Checking for full coverage of merged files...')
    for i, merged in enumerate(files_to_check):
        if math.isclose(merged[-1].isnull().sum().values, baseline, rel_tol=0.075):
            print(f'{files[i]} is fully covered.')
        else:
            print(f'{files[i]} is not fully covered. Deleting file...')
            os.remove(files[i])
            continue

def merge_observations(dates, files, dl_path):
    """Mosaic merge .tif files with same observation date."""
    merged_paths = []
    for date in dates:
        print('Merging images for date: ', date + ' in' + dl_path + '...')
        samedate_files = []
        for file in files:
            filedate = paths_to_datetimeindex([file])[0].strftime('%m-%d-%Y')
            if filedate == date:
                samedate_files.append(file)
        path = dl_path + date + '.tif'
        merged_paths.append(path)
        mosaic = gdal.Warp(path, samedate_files, format='GTiff', dstSRS='EPSG:32618', srcNodata=0, dstNodata=np.nan, multithread=True)
        mosaic = None
    quality_control(merged_paths)


#site_codes = ['CCHT']#['CCHT', 'GSHT', 'BRHT', 'COHT', 'IVHT', 'AQHT', 'MGHT', 'ARHT', 'OKHT']

site_codes = [input('Enter the site code for which your trying to merge (CCHT, CRTT, GPHT, etc.): ')]
user_input = input('Are you trying to merge images meant for model training? (True/False): ')
if user_input in ['True', 't', 'Yes']:
    DOWNLOAD_DIR_ROOT = DOWNLOAD_DIR_ROOT + 'TRAINING/'
elif user_input in ['False', 'f', 'No']:
    DOWNLOAD_DIR_ROOT = DOWNLOAD_DIR_ROOT
else:
    print("Invalid input. Please enter 'True'/'t'/'Yes' or 'False'/'f'/'No'.")

for code in site_codes:
    DOWNLOAD_DIR = DOWNLOAD_DIR_ROOT + code + '/'
    print(DOWNLOAD_DIR)
    files = find_files(DOWNLOAD_DIR)
    dates = find_dates(files)
    merge_observations(dates, files, DOWNLOAD_DIR)

#ht_files, tt_files = find_files()
#ht_dates, tt_dates = find_dates(ht_files, tt_files)
#merge_observations(ht_dates, ht_files, DOWNLOAD_DIR_HT_CARACOL)
#merge_observations(tt_dates, tt_files, DOWNLOAD_DIR_TT)