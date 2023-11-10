from .params import *
from .utils import *

import numpy as np
import pandas as pd
import rioxarray as rxr
import earthpy.plot as ep
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib import colors as colors_mat
import matplotlib.animation as animation

import seaborn as sns

def clean_season(df, yr_index):
    """Drop the NaNs from the data for distribution plotting. Takes and outputs an array from a dataframe."""
    data = np.array(df['NDVI'].iloc[yr_index])
    return data[~np.isnan(data)] 


def clean_df(row):
    """Drop the NaNs from every row in a season df for distribution plotting. Takes and outputs a row (would be an np.array) from a dataframe."""
    row = np.array(row)
    return row[~np.isnan(row)]


def get_season(month):
    """Returns the season based on provided month of the year."""
    if month >= 5 and month <= 10:
        return 'Wet'
    else:
        return 'Dry'
    
    
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
    df['water_year'] = df['year'].where(df['month'] < 10, df['year'] + 1)
    df['season'] = df['month'].apply(get_season)
    # Aggregate NDVI values per year per season.
    data = df.groupby(['water_year', 'season']).agg({'NDVI':'sum'})
    return data
    

def data_prep_box(obs, times):
    """Wrangle and process raw xarray data for boxplot."""
    # First level processing fit for ridgeplot by year and season
    data = data_prep(obs, times) 
    # Change formatting to be fit for seaborn boxplot
    data_reset = data.reset_index()
    data_reset['NDVI'] = data_reset['NDVI'].apply(np.array)
    data_reset['NDVI'] = data_reset['NDVI'].apply(clean_df)
    return data_reset.explode('NDVI')


def plot_box(data, site_code):
    """Plot a boxplot of aggregated NDVI values per season and per year."""
    palette = sns.color_palette('deep')

    fig, ax = plt.subplots()
    hue_order = ['Wet', 'Dry']
    
    sns.boxplot(data=data, x='water_year', y='NDVI', hue='season', hue_order=hue_order, palette=palette, showfliers=False, ax=ax, zorder=1);
    ax.axhline(y=0.6, color='tab:green', zorder=0)
    ax.axhline(y=0.2, color='tab:red', zorder=0)
    #ax.fill_between(x=[-1,3], y1=0.7, y2=1, alpha=0.3, color='tab:green')
    ax.set_ylim([0,1]);
    ax.set_title('Seasonal NDVI Distribution at '+site_code)
    plt.show() 


def animate_ndvi_maps(ds, times, site_code):
    """Output an animation of NDVI maps over time. NDVI values are binned into 3 categories."""
    
    colors = ['tab:red', 'tab:orange', 'tab:green', '#000000']
    bins = [0, 0.2, 0.6, 1]
    assert len(bins) == len(colors)
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bins, len(cmap.colors)-1)

    patches = [mpatches.Patch(color=colors[0], label='No Veg. NDVI < 0.2'),
            mpatches.Patch(color=colors[1], label='Moderate Veg. 0.2 < NDVI < 0.6'),
            mpatches.Patch(color=colors[2], label='Dense Veg. NDVI > 0.6'),]    


    imgs = []

    fig, ax = plt.subplots(dpi=500)
    for time in times:
        toplot = ds[time][-1]
        date = paths_to_datetimeindex([time])[0]
        season = get_season(date.month)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.legend(handles=patches, fontsize='small', loc='center', bbox_to_anchor=(0.5, -0.1), fancybox=False, ncol=3, frameon=False)
        ax.patch.set_facecolor('xkcd:white')
        text = ax.text(x=0, y=0, s=time+'\n'+str(season)+', '+str(date.year)+'\n'+site_code)
        im = ax.imshow(toplot, cmap=cmap, norm=norm, animated=True)
        imgs.append([im, text])

    ani = animation.ArtistAnimation(fig, imgs, interval=800, blit=True)
    ani.save("../outputs/movies/"+site_code+"_NDVI.mp4")



def plot_ridge(sn, color, index, ax, count):
    """Plots a singular ridge for the ridgeplot. Involves a kdeplot. interp to find height at median. a vline.
    
    sn -- data for a given season
    color -- color to plot ridge and marker.
    index -- year index we are plotting for.
    ax -- axis we are plotting on.
    count -- tracks which line in the figure we are working with.
    """
    data = clean_season(sn, index)
    k = sns.kdeplot(data, ax=ax, fill=False, common_norm=True, color=color, linewidth=1.2)
    x,y = k.get_lines()[count].get_data()
    
    mode = x[np.argmax(y)]
    f = np.interp(mode,x,y)
    ax.vlines(mode, 0, f, color=color, lw=1.5)
    
    
    y_low = np.interp(0,x,y)
    y_high = np.interp(0.7,x,y)
    ax.vlines(0, 0, y_low, color='tab:red', linestyles='dashed', lw=1.5)
    ax.vlines(0.7, 0, y_high, color='tab:green', linestyles='dashed', lw=1.5)
    
    #ax.fill_between(x,y, where=(x<0), interpolate=True, alpha=0.3, color='moccasin')
    #ax.fill_between(x,y, where=(x>0.7), interpolate=True, alpha=0.3, color='tab:green')


def sn_ridgeplots(data, site_code):
    """ Plot a ridgeplot of aggregated NDVI values per season and per year."""
    n_seasons = data.shape[0]
    fig, axs = plt.subplots(n_seasons, 1, figsize=(9, n_seasons+1), sharex=True)
    
    for i, ax in enumerate(axs):
        yr = data.iloc[i].name[0]
        season = data.iloc[i].name[1]
        
        ax.set_xlim(-0.5, 1)
        ax.text(x=-0.5, y=0.5, s=str(yr)+', '+season)
        ax.patch.set_alpha(0.0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        count = 0
        if season == 'Wet':
            plot_ridge(data, 'tab:blue', i, ax, count)
            count += 1
        else:
            plot_ridge(data, 'tab:red', i, ax, count)
            count += 1
    fig.supxlabel('Seasonal NDVI Distribution at '+site_code)

    
def yr_ridgeplots(obs, times, site_code):
    """ Plot a ridgeplot of aggregated NDVI values per year."""
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
            #try:
            wet_count-=1
                #plot_ridge(dry, 'tab:red', dry_count, ax, count)
            count += 1
                #dry_count+=1
            ax.text(x=-0.5, y=1.5, s='No wet season observations for that year.', color='tab:blue')
            continue
            """except Exception as error:
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
            ax.text(x=-0.5, y=1.5, s='No dry season observations for that year.', color='tab:red')"""

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