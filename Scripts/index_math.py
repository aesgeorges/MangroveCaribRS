import xarray as xr
import numpy as np
from tqdm import tqdm

def compute_all_indices(sites, times, time_var):
    sites, ndwiMasks = compute_ndwi(sites, times, time_var)
    sites, ndviSites = compute_ndvi(sites, times, time_var)
    sites = compute_msavi2
    return sites, ndwiMasks, ndviSites


# NDWI = (green - nir)/(green + nir) McFeeters (1996)
def compute_ndwi(sites, times, time_var):
    ndwiMasks= []
    for i,site in tqdm(enumerate(sites), desc='Computing NDWI'):
        ndwi_times = []
        for time in times:
            ndwi = (site[time][3] - site[time][7])/(site[time][3] + site[time][7])
            ndwi_times.append(xr.DataArray(ndwi, coords={'band' : 'NDWI'}))
        ndwi_arr = (xr.concat(ndwi_times, dim=time_var)).to_dataset(dim='Observation Date')
        ndwiMasks.append(ndwi_arr)
        sites[i] = xr.concat([site, ndwi_arr], dim="band")
    return sites, ndwiMasks


# NDVI = (nir - red)/(nir + red) 
def compute_ndvi(sites, times, time_var):
    ndviSites = []
    for i,site in tqdm(enumerate(sites), desc='Computing NDVI'):
        ndvi_times = []
        for time in times:
            ndvi = (site[time][7] - site[time][5])/(site[time][7] + site[time][5])
            ndvi_times.append(xr.DataArray(ndvi, coords={'band' : 'NDVI'}))
        ndvi_arr = (xr.concat(ndvi_times, dim=time_var)).to_dataset(dim='Observation Date')
        ndviSites.append(ndvi_arr)
        sites[i] = xr.concat([site, ndvi_arr], dim="band")
    return sites, ndviSites


# msavi2 = (2 * nir + 1 - sqrt( (2 * nir + 1)^2 - 8 * (nir - red) )) / 2 
def compute_msavi2(sites, times, time_var):
    for i,site in tqdm(enumerate(sites), desc='Computing MSAVI2'):
        msavi_times = []
        for time in times:
            msavi = 0.5*(2*site[time][7] + 1 - np.sqrt(np.square(2*site[time][7]+1) - 8*(site[time][7] - site[time][5])))
            msavi_times.append(xr.DataArray(msavi, coords={'band' : 'MSAVI2'}))
            #site = xr.concat([site, ndwi_arr.to_dataset()], dim="band")
        msavi_arr = (xr.concat(msavi_times, dim=time_var)).to_dataset(dim='Observation Date')
        sites[i] = xr.concat([site, msavi_arr], dim="band")
    return sites