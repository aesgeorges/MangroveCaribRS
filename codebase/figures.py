from .params import *

import numpy as np
import pandas as pd
import rioxarray as rxr
import earthpy.plot as ep
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib import colors as colors_mat

import seaborn as sns

def clean_season(df, yr_index):
    """Drop the NaNs from the data for distribution plotting. Takes and outputs an array from a dataframe."""
    data = np.array(df['NDVI'].iloc[yr_index])
    return data[~np.isnan(data)] 


def plot_ridge(sn, color, index, ax, count):
    """Plots a singular ridge for the ridgeplot. Involves a kdeplot. interp to find height at median. a vline.
    
    sn -- data for a given season
    color -- color to plot ridge and marker.
    index -- year index we are plotting for.
    ax -- axis we are plotting on.
    count -- tracks which line in the figure we are working with.
    """
    data = clean_season(sn, index)
    k = sns.kdeplot(data, ax=ax, fill=False, color=color, linewidth=1.2)
    x,y = k.get_lines()[count].get_data()
    
    mode = x[np.argmax(y)]
    f = np.interp(mode,x,y)
    ax.vlines(mode, 0, f, color=color, lw=1.2)
    
def data_prep(obs, times):
    """Wrangle and process the raw xarray data for ridgeplot."""
    # Make dataframe of NDVI array for each observation. Mark year and month for further aggregation.
    y = [obs[time][-1].values.ravel().tolist() for time in times]
    df = pd.DataFrame({
        'Date': times,
        'NDVI': y
    })
    df['year'] = pd.to_datetime(df['Date']).dt.year
    df['month'] = pd.to_datetime(df['Date']).dt.month
    # Split dataframe in wet and dry seasons.
    dfwet = df[(df['month'] >= 5) & (df['month'] <= 10)]
    dfdry = df[~(df['month'] >= 5) & (df['month'] <= 10)]
    # Aggregate NDVI values per year per season.
    wet = dfwet.groupby('year').agg({'NDVI':'sum'})
    dry = dfdry.groupby('year').agg({'NDVI':'sum'})
    return wet, dry


def ndvi_ridgeplots(obs, times, site_code):
    """ Plot a ridgeplot of aggregated NDVI values per season and per year."""
    wet, dry = data_prep(obs, times)
    
    years = np.arange(2010, 2021)
    fig, axs = plt.subplots(len(years), 1, figsize=(9,len(years)+5), sharex=True)
    dry_count=0
    wet_count=0
    for i, ax in enumerate(axs):
        ax.set_xlim(-0.5, 1)
        ax.text(x=-0.5, y=0.5, s=years[i])
        ax.patch.set_alpha(0.0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        #ax.get_xaxis().set_visible(False)
        count=0
        try:
            plot_ridge(wet, 'tab:blue', wet_count, ax, count)
            count += 1
            wet_count+=1
        except Exception as error:
            #print(error)
            try:
                wet_count-=1
                plot_ridge(dry, 'tab:red', dry_count, ax, count)
                count += 1
                dry_count+=1
                ax.text(x=-0.5, y=1.5, s='No wet season observations for that year.', color='tab:blue')
                continue
            except Exception as error:
                #print(error)
                ax.text(x=-0.5, y=0.03, s='No data for that year.', color='tab:blue')
                i-=1
                continue
        try:
            plot_ridge(dry, 'tab:red', i, ax, count)
            count += 1
            dry_count+=1
        except Exception as error:
            dry_count-=1
            #print(error)
            ax.text(x=-0.5, y=1.5, s='No dry season observations for that year.', color='tab:red')

    #fig.subplots_adjust(wspace=0, hspace=-0.5)
    patches = [mpatches.Patch(color='tab:red', label='Dry Season'),
               mpatches.Patch(color='tab:blue', label='Wet Season'),
               ]

    #fig.legend(handles=patches, fancybox=False, loc='lower right', ncol=1)
    fig.supxlabel('Seasonal NDVI Distribution at '+site_code)
    #plt.tight_layout()
    

def metrics_timeseries(df, site_code, title, ylabel):
    """ Plot the timeseries of specified health metric.
    
    df -- pandas Dataframe of metric to be plotted.
    Columns are, in order:
        datetimeindex, sitecode, ndates, timedelta, linfit
    site_code -- string name of site
    title -- string title of plot
    ylabel -- string y axis label
    """
    fig, ax = plt.subplots(figsize=(20,10))
    df.plot.scatter(x='ndates', y=site_code, ax=ax, c='tab:orange', marker='+', s=300, lw=7, zorder=5)
    df.plot(x='ndates', y='linfit', ax=ax, c='tab:blue', lw=7, alpha=0.5, label='Linear Fit', zorder=10)

    ax.set_xlim(df['ndates'].min() - timedelta(days=20), df['ndates'].max() + timedelta(days=100))

    ax.set_title(title)
    ax.set_xlabel('Observation Date')
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(zorder=0)

    # careful with saving to not overwrite old plots, leave this commented by default
    #plt.savefig('../outputs/Final Figures/ndvi_timeseries_white.png', dpi=1000, bbox_inches='tight', transparent=True)

    plt.show();
    

def metrics_visualization(metric, aoi_list, title):
    """Plot the trajectory visualization of forest health metrics (gross cover change and polar moment).
    
    metric -- pandas Dataframe holding calculated metrics for a given site.
    Columns are, in order:
         areaSites, changeSites, percChangeSites, secMOAs_x, changeMOA_x, percMOA_x,secMOAs_y, changeMOA_y, percMOA_y, secMOA_pol, changeMOA_pol, percMOA_pol 
    title -- string title of plot.
    """
    fig, ax = plt.subplots(figsize=(30,30))
    ax.set_xlabel('Gross Cover Change (km^2)')
    ax.set_ylabel('Polar Moment of Area Change (km^4)')
    
    # Start positions (X is set of gross covers at Y1, Y is set of 2MOA_pol at Y1)
    areaSites = np.array(metric[0])
    changeSites = np.array(metric[1])
    changeMOA_pol = np.array(metric[-2])
    
    U = changeSites
    V = changeMOA_pol
    print(U)
    X = [0] #(areaSites.T[0])/1e6
    Y = [0]#np.array((metric[-3])[0])/1e12
    # Magnitude is distance change (U is for gross cover change, V is for 2MOA change)
    # Color code of arrows (blue for increase in both, red for decrease in both, gray for other)
    arr_colors = []
    for i, change in enumerate(U):
        if change > 0 and V[i] > 0:
            arr_colors.append('blue')
        elif change < 0 and V [i] < 0:
            arr_colors.append('red')
        else:
            arr_colors.append('green') 
    
    ax.grid()
    ax.scatter(x=X, y=Y, c='k')
    ax.scatter(x=U, y=V, c='k', alpha=0.25)
    ax.quiver(X,Y,U,V, color=arr_colors, angles='xy', scale_units='xy', scale=1, alpha=1)
    for i, label in enumerate(aoi_list[:-1]):
        plt.annotate(label, (U[i] - 0.4, V[i] - 0.25,))

    patches = [mpatches.Patch(color='blue', label='Net Increase in Gross Cover and Distribution'),
                mpatches.Patch(color='green', label='Mixed Change'),
                mpatches.Patch(color='red', label='Net Decrease in Gross Cover and Distribution')]
    ax.legend(handles=patches, loc='upper right', borderaxespad=0.)
    ax.set_title(title)
    #ax.set_xlim(-1.8, 1.8)
    ax.patch.set_facecolor('xkcd:white')
    ax.set_axisbelow(True)