import numpy as np
import lightkurve as lk
import glob
import warnings
warnings.filterwarnings('ignore')

from astropy.timeseries import LombScargle as LS
import astropy.units as u

##########################################################################################################################

# takes lightcurve as an input
# max_f is the maxiumum frequency to evaluate periodogram at
# probability is the false alarm probability used to calculate the minimum significant power

def sig_pg_peaks(lightcurve, max_f, probability, window_size):
    
    # list of significant max power within each window
    significant_power = []
    significant_frequency = []
    significant_period =[]
    
    # define time flux, and error arrays
    t = lightcurve.time.value# * u.d
    f = lightcurve.flux.value# * u.electron / u.s
    f_err = lightcurve.flux_err.value# * u.electron / u.s
    
    # use astropy Lomb Scargle periodogram up to max frequency
    ls = LS(t, f, f_err)
    
    # calculate the peak height required to attain the input false alarm probability
    min_pwr = ls.false_alarm_level(probability, method='baluev')
    
    # window to evaluate in
    win_start = 0
    win_stop = window_size
    
    # amount to move window
    # move it by the window size
    n = window_size
    
    # analyze periodograms
    print('Starting Periodogram Analysis')
    
    while win_stop <= max_f:
        # evaluate Lomb Scargle within window
        frequency, power = ls.autopower(method='fast',
                                        minimum_frequency = win_start,
                                        maximum_frequency = win_stop)
        
        # find max power within window
        max_pwr = power.max()
        
        # add max power to list if it is significant
        if max_pwr > min_pwr:

            # find the frequency at that power
            mask = np.where(power == max_pwr)
            f = frequency[mask]
            
            # calculate the period from frequency
            p = 1/f
            
            # append power, significant frequency, and significant period to lists
            significant_power.append(max_pwr)
            significant_frequency.append(f)
            significant_period.append(p)
            
            # print values for sanity check
#             print(max_pwr, f, p)
            
            # increase window
            win_start += n
            win_stop += n
        
        else:
            # increase window
            win_start += n
            win_stop += n
            
        # end if/else statement
    # end loop
    print('Periodogram Analysis Finished')

    # concatenate lists
    significant_frequency = np.concatenate(significant_frequency).tolist()
    significant_period = np.concatenate(significant_period).tolist()

    # Calculate change in f and p per point
    delta_f = []
    delta_p = []

    for i in range(len(significant_frequency) - 1):
        n = significant_frequency[i+1] - significant_frequency[i]
        delta_f.append(n)

    for i in range(len(significant_period) - 1):
        n = significant_period[i] - significant_period[i+1]
        delta_p.append(n)
    
    return(significant_power, significant_frequency, significant_period, delta_f, delta_p)
