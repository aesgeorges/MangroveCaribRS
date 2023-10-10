from .params import *
import numpy as np
import pandas as pd
import dask


def moa_calc(inputSites, dir, times): # Inputs are region to calculate MOA on and the direction to take MOA on, dir = 'x' or 'y'
    secMOAs = []
    for j in range(len(times)):
        moa_yr = []
        for i, input in enumerate(inputSites):
            pixs = []
            # X direction MOA
            if dir == 0:
                pixs = [row.groupby(row).count()[0] for row in input[j]]
                dists = [3*((input[j].shape[0])/2 - 1 - k) for k in range(len(input[j]))]
            # Y direction MOA 
            elif dir == 1:
                pixs = [col.groupby(col).count()[0] for col in input[j].T]
                dists = [3*(((input[j].T).shape[0])/2 - 1 - k) for k in range(len(input[j].T))]
            moa = 0
            for l,pix in enumerate(pixs):
                moa += (5**2)*pix * dists[l]**2 
            moa_yr.append(moa)
        secMOAs.append(moa_yr)
    changeMOA = [(secMOAs[-1][i] - secMOAs[0][i])/1e12 for i in range(len(secMOAs[0]))]
    percMOA = [(change*100)/(secMOAs[0][i]/1e12) for i, change in enumerate(changeMOA)]

    return secMOAs, changeMOA, percMOA


def get_metrics(inputSites, times):
    pixelSites = []
    areaSites = []
    changeSites = []
    percChangeSites = []
    secMOAs_x = []
    
    # Counting Pixels for Area calculations
    for i, mask in enumerate(inputSites):
        pixels = np.array([np.size(m) - np.count_nonzero(m) for m in mask])
        pixelSites.append(pixels)
    
    # Calcualte Gross Cover Change   
    for i, pixels in enumerate(pixelSites):
        surfaces = [(5**2)*pixel_obs for pixel_obs in pixels]
        areaSites.append(surfaces)
        change = (surfaces[-1] - surfaces[1])/(1e6)
        percent = (change*100)/(surfaces[1]/1e6)
        changeSites.append(change)
        percChangeSites.append(percent)

    # Calculate MOA in x and y
    secMOAs_x, changeMOA_x, percMOA_x = moa_calc(inputSites, 0, times)
    secMOAs_y, changeMOA_y, percMOA_y = moa_calc(inputSites, 1, times)

    # Calculate Polar MOA
    secMOA_pol = []
    for i, year in enumerate(secMOAs_x):
            moa_yr = [moa_x + secMOAs_y[i][j] for j, moa_x in enumerate(year)]
            secMOA_pol.append(moa_yr)

    changeMOA_pol = [secMOA_pol[-1][i] - secMOA_pol[1][i] for i in range(len(secMOA_pol[1]))]
    percMOA_pol = [(change*100)/(secMOA_pol[1][i]) for i, change in enumerate(changeMOA_pol)] 
    
    return areaSites, changeSites, percChangeSites, secMOAs_x, changeMOA_x, percMOA_x, secMOAs_y, changeMOA_y, percMOA_y, secMOA_pol, changeMOA_pol, percMOA_pol


def ndvi_calc(times, split_sites, aoi_list):
    avg_NDVI = []
    df = pd.DataFrame(columns=aoi_list)
    for i,site in enumerate(split_sites):
        avg = [site[time][-1].mean().values for time in times]
        avg_NDVI.append(avg)
        df[aoi_list[i]] = avg
    df['dates'] = [datetime.strptime(date, '%m-%d-%Y').date() for date in times] 
    return df    


@dask.delayed
def uvvr_calc(times, unvegSites, mangroveSites, aoi_list):
    unvegArea = get_metrics(unvegSites, times)[0]
    vegArea = get_metrics(mangroveSites, times)[0]
    uvvrSites = []

    df_uvvr = pd.DataFrame(columns=aoi_list)
    for i,site in enumerate(unvegArea):
        uvvr = np.array(site) / np.array(vegArea[i])
        uvvrSites.append(uvvr)
        df_uvvr[aoi_list[i]] = np.array(uvvr)
    df_uvvr['dates'] = [datetime.strptime(date, '%m-%d-%Y').date() for date in times]
    return df_uvvr