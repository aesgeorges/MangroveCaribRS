import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
from matplotlib import colors as colors_mat

import earthpy as ep
import numpy as np

import seaborn as sns

# Color values for custom cmaps
custom_cmap = colors_mat.ListedColormap(colors=['#1f78b4', '#488f52', '#a6cee3', '#8e3b00', '#fdbf6f', '#f7fcf5', '#00ff11', '#8115d3'])
boundaries = [0, 1, 2, 3, 4, 5, 6, 7]
custom_norm = colors_mat.BoundaryNorm(boundaries, custom_cmap.N, clip=True)

patches = [mpatches.Patch(color='#1f78b4', label='Water'),
            mpatches.Patch(color='#488f52', label='Mangrove'),
            mpatches.Patch(color='#a6cee3', label='Salt Flat'),
            mpatches.Patch(color='#8e3b00', label='Mud Flat'),
            mpatches.Patch(color='#fdbf6f', label='Soil'),
            mpatches.Patch(color='#f7fcf5', label='Sand'),
            mpatches.Patch(color='#00ff11', label='Crops'),
            mpatches.Patch(color='#8115d3', label='Urban')]

# Function to plot visualizations of all sites
def plot_all(sites_toplot, aoi_list, cmap):
    fig, axs = plt.subplots(2,3, figsize=(12,16))
    axs = list(itertools.chain.from_iterable(axs))
    count = 0
    print('check')
    for j,blur in enumerate(sites_toplot):
        for ob in blur:
            nd = axs[count].imshow(ob, cmap=cmap)
            axs[count].set_xticklabels([])
            axs[count].set_yticklabels([])
            axs[count].set_title(aoi_list[j])
            plt.colorbar(nd, ax = axs[count])
            count+=1
    plt.show()


# Function to only plot mangrove cover
def plot_mangrove(mangroveSites, sites, aoi_list, times):
    fig, axs = plt.subplots(2,2, figsize=(15,15))
    axs = list(itertools.chain.from_iterable(axs))
    custom_cmap = colors_mat.ListedColormap(['#0025FC', '#D7262F', '#BBDFCB'])

    patches = [mpatches.Patch(color='#D7262F', label='Coastal and Mangrove Retreat'),
                mpatches.Patch(color='#BBDFCB', label='No Change in Cover'),
                mpatches.Patch(color='#0025FC', label='Gained Mangrove Cover')]

    for i,site in enumerate(mangroveSites):
        ep.plot_rgb(sites[i][times[-1]], rgb=[5,3,1], stretch=True,
                str_clip=.09, ax=axs[i])
        # Apply the blurred Image mask to NDVI !!!!!
        first = site[0]
        last = site[-1]
        first = np.where(site[0] == 1, 4, 0)
        last = np.where(site[-2] == 1, 2, 0)
        change = first + last
        change_mask = np.ma.masked_where(change == 0, change)
        axs[i].imshow(change_mask, cmap=custom_cmap)
        axs[i].set_title(aoi_list[i])
        
    fig.legend(handles=patches, fontsize='small')
    fig.suptitle('Mangrove Cover Change between '+times[0]+' and '+times[-2])
    fig.patch.set_facecolor('xkcd:white')
    fig.delaxes(axs[-1])
    #fig.delaxes(axs[-2])
    plt.tight_layout(h_pad=5, w_pad=-15)
    plt.show()

# Function to plot grid metric figure
def metrics_visualization(metric, title, aoi_list):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xlabel('Gross Cover (km^2)')
    ax.set_ylabel('Polar Moment of Area (km^4)')
    # Start positions (X is set of gross covers at Y1, Y is set of 2MOA_pol at Y1)
    areaSites = np.array(metric[0])
    X = (areaSites.T[0])/1e6
    Y = np.array((metric[-3])[0])/1e12
    # Magnitude is distance change (U is for gross cover change, V is for 2MOA change)
    U = metric[1]
    V = np.array(metric[-2])/1e12
    # Color code of arrows (blue for increase in both, red for decrease in both, gray for other)
    arr_colors = []
    for i, change in enumerate(metric[1]):
        if change > 0 and (metric[-2])[i] > 0:
            arr_colors.append('blue')
        elif change < 0 and (metric[-2])[i] < 0:
            arr_colors.append('red')
        else:
            arr_colors.append('green') 
    ax.grid()
    ax.scatter(x=X, y=Y, c='k')
    ax.scatter(x=areaSites.T[-1]/1e6, y=np.array((metric[-3])[-1])/1e12, c='k', alpha=0.25)
    ax.quiver(X,Y,U,V, color=arr_colors, angles='xy', scale_units='xy', scale=1)
    for i, label in enumerate(aoi_list):
        plt.annotate(label, (X[i] + 0.005, Y[i] - 0.25,))

    patches = [mpatches.Patch(color='blue', label='Net Increase in Gross Cover and Distribution'),
                mpatches.Patch(color='green', label='Mixed Change'),
                mpatches.Patch(color='red', label='Net Decrease in Gross Cover and Distribution')]
    ax.legend(handles=patches, loc='lower right', borderaxespad=0.)
    ax.set_title(title)
    ax.patch.set_facecolor('xkcd:white')
    ax.set_axisbelow(True)