from .params import PATTERN_REGEX
import re, glob
from datetime import datetime

def aoi_path(name):
    """Return the string path of a shapefile from its string name."""
    return '../datasets/Shapefiles/'+name+'.shp'


def sort_observations(data_dir):
    """Return the sorted list of observations from a directory.
    
    data_dir -- directory hosting observation files.
    """
    # Obtain file names using glob.glob
    files = glob.glob(data_dir)
    date_pattern = r'(\d{2}-\d{2}-\d{4})' #mm-dd-yyy
    # Convert filenames to datetime format
    dates = [re.search(date_pattern, file).group(1) for file in files]
    dates = [datetime.strptime(date, '%m-%d-%Y') for date in dates]
    # Sort the files based on dates
    sorted_files = [file for _, file in sorted(zip(dates, files))]
    return sorted_files

def paths_to_datetimeindex(list):
    """Convert the names of file to datetime. Return list of all observation dates.
    
    Files are named following a convention captured in PATTERN_REGEX (MM-DD-YYY).
    
    list -- list of file names.
    new_list -- list of datetimes corresponding to list.
    """
    pattern = PATTERN_REGEX
    new_list = []
    for item in list:
        time = re.search(pattern, item).group(1)
        time = datetime.strptime(time, '%m-%d-%Y').date()
        new_list.append(time)
    new_list = sorted(new_list)    
    return new_list