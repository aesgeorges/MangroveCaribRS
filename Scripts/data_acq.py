import xarray as xr
import geopandas as gpd
import rioxarray as rxr
import glob, re, datetime

data_dir = 'E:/PhD Data/Planet 3m/*.TIF'
sites = []
resSites = []


band_titles = ['CoastalBlue', 'Blue', 'Green1', 'Green', 'Yellow', 'Red', 'RedEdge', 'NIR']
band_names = {'band':{1: 'CoastalBlue',
                              2: 'Blue',
                              3: 'Green1',
                              4: 'Green',
                              5: 'Yellow',
                              6: 'Red',
                              7: 'RedEdge',
                              8: 'NIR'
                }}
pos_var = xr.Variable('Position', ['Ob1','Ob2','Ob3','Ob4','Ob5','Ob6','Ob7'])


# Find dates of input geotiff files
def paths_to_datetimeindex(list):
    pattern = r'.*(\d{4}-\d{2}-\d{2}).*'
    new_list = []
    for item in list:
        time = re.search(pattern, item).group(1)
        time = datetime.datetime.strptime(time, '%Y-%m-%d').date()
        new_list.append(time)
    new_list = sorted(new_list)    
    return new_list

times = [i.strftime('%m/%d/%Y') for i in paths_to_datetimeindex(glob.glob(data_dir))]
time_var = xr.Variable('Observation Date', times)

def pull_data(aoi_list):
    for area in aoi_list:
        aoi = gpd.read_file(area)
        geotiffs_da = xr.concat(
            [rxr.open_rasterio(entry).rio.clip(aoi.geometry, from_disk=True).squeeze() 
            for entry in glob.glob(data_dir)], dim=time_var)
        area_ds = geotiffs_da.to_dataset(dim='Observation Date')
        sites.append(area_ds)
        resSites.append(area_ds.rio.resolution()[0])
    return sites, resSites