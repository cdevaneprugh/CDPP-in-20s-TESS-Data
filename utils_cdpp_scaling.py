import numpy as np

# cdpp scaling from christiansen 2012
# t_dur is the desired transit time to scale official cdpp value to
# t_cdpp is the closest official transit time to t_dur
# cdpp_n is the official cdpp value calculated by the TPS at transit time t_cdpp

# see page 12 of Christiansen 2012 for more detail

def scale_cdpp(t_cdpp, t_dur, cdpp_n):
    return np.sqrt(t_cdpp/t_dur) * cdpp_n