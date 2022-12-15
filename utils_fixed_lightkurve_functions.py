import numpy as np
import warnings
from lightkurve.utils import running_mean
from astropy.stats.sigma_clipping import sigma_clip

#--------------------------------------------------------------------------------------------------------

# fixed version of lightkurve's sigma clipping

def remove_outliers(self, sigma=5.0, sigma_lower=None, sigma_upper=None, return_mask=False, **kwargs):
    
    # First, we create the outlier mask using AstroPy's sigma_clip function
    with warnings.catch_warnings():  # Ignore warnings due to NaNs or Infs
        warnings.simplefilter("ignore")
        
        outlier_mask = sigma_clip(
            data=self.flux.value, # use unitless array to fix lk bug
            sigma=sigma,
            sigma_lower=sigma_lower,
            sigma_upper=sigma_upper,
            **kwargs,
        ).mask
        
        # Second, we return the masked light curve and optionally the mask itself
        if return_mask:
            return self.copy()[~outlier_mask], outlier_mask
        return self.copy()[~outlier_mask]

#--------------------------------------------------------------------------------------------------------

# cdpp calculation from lightkurve, fixed to use my sigma clipping 

def estimate_cdpp(self, transit_duration=13, savgol_window=101, savgol_polyorder=2, sigma=5.0) -> float:
    
    # check that transit duration is an int
    if not isinstance(transit_duration, int):
        raise ValueError(
            "transit_duration must be an integer in units "
            "number of cadences, got {}.".format(transit_duration)
        )

    detrended_lc = self.flatten(window_length=savgol_window, polyorder=savgol_polyorder)
    
    cleaned_lc = remove_outliers(detrended_lc, sigma = sigma)
    
    # normalize and ignore warnings
    with warnings.catch_warnings():  # ignore "already normalized" message
        warnings.filterwarnings("ignore", message=".*already.*")
        normalized_lc = cleaned_lc.normalize("ppm")
    
    # calculate running mean
    mean = running_mean(data=normalized_lc.flux.value, window_size=transit_duration)
    return np.std(mean).item()
