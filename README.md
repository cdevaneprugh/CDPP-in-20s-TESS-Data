# CDPP-in-20s-TESS-Data

# Data
In the data folder there’s the original curl script from NASA, as well as one to only download the 20 second cadence light curves. If you need to download all the light curves for some reason, you can use utils_fast-lc_sorting.py to sort them all into folders that the rest of my code is set up to interact with. The parent directory for the light curve files needs to be names ‘fast_lc’ for everything to work.

The target_info.csv file has basic properties like the TICID, group number, magnitude, logg, etc. Additionally, it has the mean, and median precalculated CDPP values from all available sectors for each target. There are two other files, lightkurve_estimated_cdpp.csv, and scaled_effective_cdpp.csv. Both of these have the cdpp calculations/scalings for transit times from 1 minute to 1 hour for all stars in our sample. Rather than use the lightkurve function to calculate the values (which is really really slow) it’s probably better to just pull the calculations straight from these csv files.

# Code
In order, the python scripts and their general purpose are listed. Also the code is well documented throughout for things like what input variables, and what data type a function needs.

1. main_cdpp_calculations - Script that ran all the calculations for  lightkurve_estimated_cdpp.csv and scaled_effective_cdpp.csv

2. utils_cdpp_meta_data - Functions that pull the various meta data related to cdpp from the fits headers.

3. utils_cdpp_scaling - Scales TPS cdpp values via methods in Christiansen 2012

4. utils_data_prep - Various functions to clean up light curves for cdpp calculations, periodogram analysis, plotting, etc.

5. utils_fast-lc_sorting - Sorts all the light curves downloaded by the fast-lc_curl_script

6. utils_fixed_lightkurve_functions - Fixed versions of the sigma clipping and cdpp estimation tools from lightkurve.

7. utils_magnitude_correction - Uses Scipy’s curve fitting and the exponential function from Kunimoto 2022 to magnitude correct the cdpp values.

8. utils_periodogram_analysis - PErforms a Lomb Scargle fourier transform, then looks for significant peaks in a light curve’s periodogram.

9. utils_plot_all_sectors - Used at the beginning of the summer. Plots all sectors of a target as subplots so we could look at each sector.
