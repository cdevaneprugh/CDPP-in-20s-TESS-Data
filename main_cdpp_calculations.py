"""Scale cdpp via the christiansen method and estimate with lightkurve for transit times
of 1 min to 1 hour. Combines both into a single, exported csv."""

import numpy as np
import pandas as pd
from utils_data_prep import prep_data
from utils_fixed_lightkurve_functions import estimate_cdpp

# import csv files
info = pd.read_csv('target_info.csv')

# define targets
targets = np.asarray(info.ticid)
targets = [str(i) for i in targets]
print(len(targets),'targets')
print()

# times to calculate cdpp at
times = np.arange(1, 61, 1) # in minutes

# convert to number of cadences
transit_times = times * 60 / 20
transit_times = [int(i) for i in transit_times] # must be an int

# add times to empty data frame
data = {'transit_time':times}
df = pd.DataFrame(data=data)

star_count = 0

# calculate and scale cdpp values
for tic in targets:
    star_count += 1

    # step 1 prep lightcurve for target
    lc = prep_lightcurves(tic, True, 1)
    print(f'{tic} lightcurve prepped')
    
    # step 2 calculate cdpp from list of times
    lk_cdpp = []
    for t in transit_times:
        n = estimate_cdpp(lc, transit_duration=t, savgol_window=8997) # lk/gilliland method
        lk_cdpp.append(n)
    
    print(f'{tic} cdpp calculated')
    
    # step 3 scale existing cdpp via christiansen method
    mask = np.where( info.ticid == int(tic) ) # define cdpp values to scale from
    target_30m_cdpp = np.asarray(info.CDPP0_5_mean)[mask]
    target_60m_cdpp = np.asarray(info.CDPP1_0_mean)[mask]
    
    times_30 = np.arange(1,46,1) # times to scale cdpp to
    times_60 = np.arange(46,61,1)

    scaled_cdpp_30 = np.sqrt(30/times_30) * target_30m_cdpp # scale cdpp values
    scaled_cdpp_60 = np.sqrt(60/times_60) * target_60m_cdpp
    
    eff_cdpp = np.concatenate( (scaled_cdpp_30, scaled_cdpp_60) ) # concatenate arrays
    
    print(f'{tic} cdpp scaled')
    
    # step 4 add columns to data frame
    df[f'{tic}_lk'] = lk_cdpp
    df[f'{tic}_scaled'] = eff_cdpp
    
    print('star', star_count, 'complete')
    print()

# export final csv
df.to_csv('data/calculated_cdpp_values.csv', index=False)
