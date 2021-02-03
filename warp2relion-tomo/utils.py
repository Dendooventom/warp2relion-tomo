import numpy as np


def read_tlt_file(tlt_file):
    """Read an imod format .tlt file into a 1 dimensional numpy array
    """
    tilt_angles = np.loadtxt(tlt_file)
    return tilt_angles
