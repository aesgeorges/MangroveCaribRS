"""
[Supervised Workflow] Remote Sensing Analysis of Mangrove Forest Health and Extent Script <hr>
Written by Alexandre Erich Sebastien Georges, PhD Student at UC Berkeley in EFMH-Civil and Environmental Engineering, January 2023

"""

import os, pickle, itertools, glob, re, datetime
import tkinter as tk
from tkinter import filedialog

import xarray as xr
import geopandas as gpd
import rioxarray as rxr

from plot_funcs import *
from index_math import *
from data_acq import *

root = tk.Tk()

aoi_list = filedialog.askopenfilenames(title='Please input the AOIs .shp files', filetypes=[('Shapefiles', '*.shp')])

sites, resSites = pull_data(aoi_list)

sites, ndwiMasks, ndviSites = compute_all_indices(sites, times, time_var)

print('test')