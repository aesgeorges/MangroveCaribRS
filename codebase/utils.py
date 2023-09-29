from .params import PATTERN_REGEX
import re
from datetime import datetime

def aoi_path(name):
    """Return the string path of a shapefile from its string name."""
    return '../datasets/Shapefiles/'+name+'.shp'

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