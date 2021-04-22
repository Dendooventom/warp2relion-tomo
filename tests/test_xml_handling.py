from pathlib import Path
import numpy as np

from warp2reliontomo.utils import xml2dict, TiltSeriesXMLHandler


test_data_directory = Path(__file__).parent.parent / 'test_data'
tilt_series_xml = test_data_directory / 'TS_02.mrc.xml'


def test_xml2dict():
    data = xml2dict(tilt_series_xml)
    assert isinstance(data, dict)
    assert 'TiltSeries' in data.keys()


def test_original_tilt_angles():
    tilt_angles = TiltSeriesXMLHandler(tilt_series_xml).original_tilt_angles
    assert isinstance(tilt_angles, np.ndarray)
    assert len(tilt_angles) == 102
    assert tilt_angles[0] == -40.73


def test_defoci():
    defoci = TiltSeriesXMLHandler(tilt_series_xml).defoci
    assert isinstance(defoci, np.ndarray)
    assert len(defoci) == 102
    assert defoci.dtype == float

def test():
    xml = TiltSeriesXMLHandler(tilt_series_xml)
    4