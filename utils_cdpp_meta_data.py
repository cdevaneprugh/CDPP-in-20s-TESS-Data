import numpy as np
import pandas as pd
from astropy.io import fits
import glob

#-------------------------------------------------------------------------------------

# simple function to pull a cdpp value stored in a fits header
def yank_cdpp(filename, cdpp_time):
    file = fits.open(filename)
    cdpp = file[1].header[cdpp_time]
    return cdpp

#-------------------------------------------------------------------------------------

# pre calculated cdpp stats over all sectors in globbed list
def cdpp_stats(target, cdpp_time):
    target = str(target)
    
    # glob and sort files
    files = glob.glob(f'data/fast_lc/{target}/*')
    files = np.sort(files)
    
    # append cdpp values from file header to list
    values = []
    for fn in files:
        file = fits.open(fn)
        values.append( file[1].header[cdpp_time] )
    
    # statistics to return
    mean_val = np.mean( values )
    med_val = np.median( values )
    std_val = np.std( values )
    
    return mean_val, med_val, std_val

#-------------------------------------------------------------------------------------

# function to pull all cdpp values for targets based on group number
# should add cdpp values as a list to a dictionary where ticid is the corresponding key

def group_cdpp_yank(group):
    
    # import target info
    df = pd.read_csv('data/target_info.csv')
    
    # mask off targets in group
    mask = np.where(df.group == group)
    group = np.asarray(df.ticid)[mask]
    
    # convert target list to strings
    targets = [str(i) for i in group]
    
    #cdpp times to pull from header
    cdpp_times = ['CDPP0_5', 'CDPP1_0', 'CDPP2_0'] 
    
    # empty dictionary to hold everything
    Dict = {}
    
    #--------------------------------------------------------
    # loop through each target
    # append mean cdpp of all files
    for target in targets:
    
        # empty list for avg cdpp values of each target
        avg_cdpp_values = []
    
        # mean cdpp value for each time in cdpp_times
        for time in cdpp_times:
            avg_cdpp_values.append( mean_cdpp(target, time) )
    
        # add mean cdpp to dictionary w/ target as its key
        Dict[target] = avg_cdpp_values
    #--------------------------------------------------------

    return Dict # return the dictionary

#-------------------------------------------------------------------------------------

# grabs ticid for all targets in input groups
def yank_ticid(groups):
    df = pd.read_csv('data/target_info.csv')

    d = {}
    for group in groups:
        # mask ticid where group is
        mask = np.where(df.group == group)
        tics = np.asarray(df.ticid)[mask]
        
        targets = [str(i) for i in tics] # convert ticid to str
        d[group] = targets # add to dictionary
    
    # returns dictionary if multiple groups
    if len(groups) > 1:
        return d
    else:
        return d[group] # returns list of targets for single group