from scipy.optimize import curve_fit

# curve paper
def g(M, a, b, c):
    second_term = b * 10.**(0.2*(M-10.))
    third_term = c * 10.**(0.4*(M-10.))
    return a + second_term + third_term


# magnitude must be in ascending order
# cdpp should be sorted based on magnitude array as well
def correct_magnitude(magnitude, cdpp):
    
    # use scipy's fitting
    popt, pcov = curve_fit(g, magnitude, cdpp)
    
    # make list of corrections
    correction = []
    for i in magnitude:
        correction.append( g(i, popt[0], popt[1], popt[2]) )
    
    # apply corrections to cdpp
    corrected_cdpp = cdpp - correction
    
    return correction, corrected_cdpp