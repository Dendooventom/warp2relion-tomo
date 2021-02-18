from pathlib import Path

import numpy as np

from warp2reliontomo.utils import xml2dict, get_original_tilt_angles

test_data_directory = Path(__file__).parent.parent / 'test_data'
tilt_series_xml = test_data_directory / 'TS_02.mrc.xml'

data = xml2dict(tilt_series_xml)


def test_get_original_tilt_angles():
    tilt_angles = get_original_tilt_angles(data)
    assert isinstance(tilt_angles, np.ndarray)
    assert len(tilt_angles) == 102
    assert tilt_angles[0]==-40.73
