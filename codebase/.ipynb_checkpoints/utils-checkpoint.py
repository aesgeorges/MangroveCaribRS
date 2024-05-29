import re, glob
import xarray as xr
import rioxarray as rxr
from numpy import testing
from datetime import datetime
from .params import PATTERN_REGEX, DOWNLOAD_DIR_ROOT

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


def align_coords(da1, da2):
    """
    Double check that items have the same (more like close) x and y values in the coords. If not, adjust by moving the coordinates of one to the other.
    
    Only use this after making sure there's no other issues with the images AOIs and projections.
    Shoutout Ann Scheliga for this piece of code. 
    """
    coord_names = ['x', 'y']
    for coord in coord_names:
        try:
            testing.assert_allclose(da1[coord].values, da2[coord].values)
        except AssertionError:
            #print(f"Matching {coord}-coordinates")
            da2[coord] = da1[coord]
    return da1, da2


def align_dataset(site_dir):
    """
    Check if coordinates values in x and y align with images in folder, if not, align them to the first image in the directory.
    
    files -- path to directory containing GeoTIFFs, contains regex rule for all .TIF files
    Returns list of all opened rasters to be concatenated later.
    """
    # Load all images in directory in memory
    images = [rxr.open_rasterio(entry).squeeze() for entry in sort_observations(site_dir)]
    # Isolate first image from directory and add to new aligned array
    new_imgs = [images[0]]
    # Check remaining for alignment with the first one, and fix accordingly
    for img in images[1:]:
        images[0], img = align_coords(images[0], img)
        new_imgs.append(img)
    return new_imgs


def mask_dataset(obs, ds):
    """Return dataset of observations with mangrove masked in."""
    return obs.where(~ds['mangrove'].isel(time=0))


def export_map_to_raster(data, site_code, path, description):
    """
    Exports generated spatial mangrove cover/health data to GeoTiff for further post-processing in QGIS/ArcGIS.
    
    data - [float32 np.array] data to be exported
    site_code - [str] location to be used
    path - [str] filepath to output
    """
    # Pull example raster from unput images for metadata recreation
    example_dir = DOWNLOAD_DIR_ROOT + site_code + '/'+ '*.tif' 
    example_raster = rxr.open_rasterio(sort_observations(example_dir)[0])
    transform = example_raster.rio.transform()
    crs = example_raster.rio.crs
    height, width = example_raster.shape[1], example_raster.shape[2]
    # Metadata
    metadata = {
        'driver': 'GTiff',
        'height': height,
        'width': width,
        'count': 1,
        'dtype': data.dtype.name,  # Use datatype of new/processed data. Ensure dtype is float32, is a string
        'crs': crs,
        'transform': transform
    }
    # Build xr.Dataset to be exported
    export_ds = xr.DataArray(
        data=data,
        dims=['y','x'],
        coords=dict(
            x=example_raster.x.data,
            y=example_raster.y.data,
        ),
        attrs=dict(
            description=description
        )
    ).to_dataset(name='mangrove_change')
    # Export
    export_ds.rio.to_raster(raster_path=path, metadata=metadata)