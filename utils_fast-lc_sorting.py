"""Sort all the fits files downloaded by the fast-lc curl script"""

import numpy as np
import glob
import os
from astropy.io import fits

file_list = glob.glob('tess*.fits')
print('Total Files:', len(file_list))

# create list of targets

targets = []
for i in range(len(file_list)):

    # use astropy to pull target ID from the fits header
    file = fits.getheader(file_list[i])

    # append target ID to targets list
    targets.append(file['TICID'])

# create list of unique targets in data set
id_list = np.unique(targets)

print("Unique Targets:", len(id_list))

# convert list to strings
id_list = [str(i) for i in id_list]

# create folder for each target
for i in range(len(id_list)):
    os.mkdir(str(id_list[i]))

# move files to their matching folders
for i in range(len(id_list)):

    # glob files to be moved
    path = '*' + str(id_list[i]) + '*.fits'
    files = glob.glob(path)

    # move and rename each individual file in files list
    for j in range(len(files)):

        # pull sector number from fits file
        sector = fits.getheader(files[j])['SECTOR']

        # define a new name for the file
        new_name = str(sector) + '_' + str(id_list[i]) + '_fast-lc.fits'

        # full path of file destination
        destination = str(id_list[i]) + '/' + new_name

        # the source path for os.rename
        source = files[j]

        # use os.rename() to move files
        os.rename(source, destination)
