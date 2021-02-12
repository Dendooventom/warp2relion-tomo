from pathlib import Path

from warp2reliontomo.parse_warp_xml import xml2dict

test_data_directory = Path(__file__).parent.parent / 'test_data'
tilt_series_xml = test_data_directory / 'TS_02.mrc.xml'


def test_xml2dict():
    data = xml2dict(tilt_series_xml)
    assert isinstance(data, dict)
