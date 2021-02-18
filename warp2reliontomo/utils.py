import numpy as np
import xml.dom.minidom as minidom

from warp2reliontomo.parse_warp_xml import parse_xml_node


def read_tlt_file(tlt_file):
    """Read an imod format .tlt file into a 1 dimensional numpy array
    """
    tilt_angles = np.loadtxt(tlt_file)
    return tilt_angles


def xml2dict(xml_path):
    """
    parse an xml metadata file of a Warp tilt-series image
    return a dictionary containing the metadata
    """
    document = minidom.parse(str(xml_path))
    return parse_xml_node(document)


def get_original_tilt_angles(xml_dict):
    """
    Get tilt angles from xml dictionary, check if they are inverted, inverted them back
    """
    tilt_angles = xml_dict['TiltSeries']['Angles'][None].astype(float)
    if xml_dict['TiltSeries']['AreAnglesInverted'] == 'True':
        tilt_angles = tilt_angles * -1
    return tilt_angles



def get_ctf_info(xml_dict):
    ctf_info = xml_dict['TiltSeries']['GridCTF']
    n_tilts = int(ctf_info['Depth'])
    defoci = []
    for i in range(n_tilts):
        key = ('0', '0', f'{i}')
        value = float(ctf_info[key])
        defoci.append(value)
    return np.array(defoci)
