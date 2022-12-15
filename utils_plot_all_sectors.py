"""Plots all sectors of a specified target within a single image. The sectors
will be plotted under each other in a vertical 'list.'"""

import numpy as np
import lightkurve as lk
import glob
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

###################################################################################
# define a function to create lightcurves for all sectors of a given target
# then plot all of those sectors within a single image for easy viewing

# take the TICID and output folder name as inputs
def plot_all(target_id, output_folder):
    # create empty lists for lc attributes
    flux = []
    time = []
    sector = []

    # glob files in target folder
    files = glob.glob('tess_fastlc_data/' + target_id + '/*.fits')

    # sort data
    files = np.sort(files)

    # loop to pull data from files
    for i in files:

        # read in lightcurve
        lc = lk.read(i)

        # remove nans and outliers
        lc = lc.remove_nans()
        lc = lc.remove_outliers()

        # add flux, time, and sector to the empty lists
        flux.append(lc.flux.value)
        time.append(lc.time.value)
        sector.append(lc.meta['SECTOR'])

        # delete variable to not kill RAM
        del lc

    # plot all sectors in a single image
    fig, axs = plt.subplots(len(sector), figsize=(20,50), constrained_layout=True)

    # title should be the TESS ID for the star
    #fig.suptitle('TICID:' + target_id, fontsize=20)

    for i in range(len(sector)):
        axs[i].plot(time[i], flux[i], 'o', color='k')
        axs[i].set_title(str(sector[i]) + ' - ' + target_id, fontsize=18)
        #axs[i].set_xlabel('Time [Days]', fontsize=14)
        #axs[i].set_ylabel('Flux', fontsize=14)

    plt.savefig(output_folder + '/' + target_id + ' - all sectors')

##################################################################################

# load in list of targets from text file
targets = np.loadtxt('target_list.txt', dtype=str)

# loop through target list, generating light curves for each target
save_folder = 'all_sectors'

for target in targets:
    plot_all(target, save_folder)
    print(target + ' completed')
