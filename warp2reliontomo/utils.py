import xml.dom.minidom as minidom
from functools import cached_property

import numpy as np

from parse_warp_xml import parse_xml_node


def xml2dict(xml_path):
    """
    parse an xml metadata file of a Warp tilt-series image
    return a dictionary containing the metadata
    """
    document = minidom.parse(str(xml_path))
    return parse_xml_node(document)


class TiltSeriesXMLHandler:
    def __init__(self, warp_ts_xml_file):
        self.file = warp_ts_xml_file

    @cached_property
    def raw_data(self):
        return xml2dict(self.file)['TiltSeries']

    @property
    def tomogram_file(self):
        return str(self.file).replace('.xml', '')

    @property
    def acceleration_voltage(self):
        """keV"""
        return float(self.raw_data['CTF']['Voltage'])

    @property
    def spherical_aberration(self):
        """mm"""
        return float(self.raw_data['CTF']['Cs'])

    @property
    def amplitude_contrast(self):
        return float(self.raw_data['CTF']['Amplitude'])

    @property
    def pixel_size(self):
        """Angstroms"""
        return float(self.raw_data['CTF']['PixelSize'])

    @property
    def window_size(self):
        """sidelength of PS used for defocus determination (Px)"""
        return int(self.raw_data['OptionsCTF']['Window'])

    @property
    def defocus_search_min(self):
        """micrometers"""
        return float(self.raw_data['OptionsCTF']['ZMin'])

    @property
    def defocus_search_max(self):
        """micrometers"""
        return float(self.raw_data['OptionsCTF']['ZMax'])

    @property
    def search_range_min(self):
        """cycles per pixel"""
        return float(self.raw_data['OptionsCTF']['RangeMin'])

    @property
    def search_range_max(self):
        """cycles per pixel"""
        return float(self.raw_data['OptionsCTF']['RangeMax'])

    @property
    def n_tilts(self):
        return len(self.raw_data['Dose'][None])

    @property
    def original_tilt_angles(self):
        """Get tilt angles from xml dictionary.
        If angles have been inverted by Warp, invert them back
        """
        tilt_angles = self.raw_data['Angles'][None].astype(float)
        if self.raw_data['AreAnglesInverted'] == 'True':
            tilt_angles = tilt_angles * -1
        return tilt_angles

    @property
    def defoci(self):
        """Defocus of each image in the tilt-series (in micrometers)
        """
        return self.extract_per_tilt_property('GridCTF')

    @property
    def defocus_deltas(self):
        """Defocus deltas (micrometers)
        """
        return self.extract_per_tilt_property('GridCTFDefocusDelta')

    @property
    def astigmatism_angles(self):
        """Defocus angles (degrees)
        """
        return self.extract_per_tilt_property('GridCTFDefocusAngle')

    @property
    def ctf_phases(self):
        """CTF phases (degrees? maybe)"""
        return self.extract_per_tilt_property('GridCTFPhase')

    def extract_per_tilt_property(self, property_name):
        data_raw = self.raw_data[property_name]
        data = [data_raw[('0', '0', f'{i}')] for i in range(self.n_tilts)]
        return np.array(data, dtype=float)


class CTFFindWriter:
    """Write a CTFFind4 output file from a Warp XML file"""

    def __init__(self, warp_xml_file):
        self.xml = TiltSeriesXMLHandler(warp_xml_file)

    @property
    def header(self):
        return '\n'.join([self.l1, self.l2, self.l3, self.l4, self.l5])

    @property
    def body(self):
        body = np.zeros((self.xml.n_tilts, 7))
        body[:, 0] = np.arange(self.xml.n_tilts) + 1
        body[:, 1] = self.defocus_max_angstrom
        body[:, 2] = self.defocus_min_angstrom
        body[:, 3] = self.astigmatism_angle_radians  # unsure of angle convention...
        body[:, 4] = self.phase_shift_radians
        # leave columns 6 and 7 (cc and fit quality)
        return body

    def write_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.header)
            f.write('\n')
            np.savetxt(f, self.body, fmt='%.6f', delimiter=' ')

    @property
    def defocus_min_angstrom(self):
        return (self.xml.defoci - (self.xml.defocus_deltas / 2)) * 1e4

    @property
    def defocus_max_angstrom(self):
        return (self.xml.defoci + (self.xml.defocus_deltas / 2)) * 1e4

    @property
    def astigmatism_angle_radians(self):
        return np.deg2rad(self.xml.astigmatism_angles)

    @property
    def phase_shift_radians(self):
        return np.deg2rad(self.xml.ctf_phases)

    @property
    def l1(self):
        return '# CTFFind style output from warp2relion-tomo'

    @property
    def l2(self):
        return f'Input file: {self.xml.tomogram_file} ; Number of micrographs: {self.xml.n_tilts}'

    @property
    def l3(self):
        pixel_size = f'Pixel size: {self.xml.pixel_size} Angstroms'
        acceleration_voltage = f'acceleration voltage: {self.xml.acceleration_voltage} keV'
        spherical_abberation = f'spherical aberration: {self.xml.spherical_aberration} mm'
        amplitude_contrast = f'amplitude contrast: {self.xml.amplitude_contrast}'
        return f'# {pixel_size} ; {acceleration_voltage} ; {spherical_abberation} ; {amplitude_contrast}'

    @property
    def l4(self):
        box_size = f'Box size: {self.xml.window_size} pixels'

        min_res = self.cycles_per_pixel_to_angstroms(self.xml.search_range_min)
        min_res = f'min. res.: {min_res} Angstroms'
        max_res = self.cycles_per_pixel_to_angstroms(self.xml.search_range_max)
        max_res = f'max. res.: {max_res} Angstroms'

        min_defocus = np.min(self.xml.defoci)
        min_defocus = f'min. def.: {min_defocus} um'
        max_defocus = np.max(self.xml.defoci)
        max_defocus = f'max. def. {max_defocus} um'
        return f'# {box_size} ; {min_res} ; {max_res} ; {min_defocus} ; {max_defocus}'

    @property
    def l5(self):
        return "# Columns: #1 - micrograph number; #2 - defocus 1 [Angstroms]; #3 - defocus 2; #4 - azimuth of astigmatism; #5 - additional phase shift [radians]; #6 - cross correlation; #7 - spacing (in Angstroms) up to which CTF rings were fit successfully"

    def cycles_per_pixel_to_angstroms(self, spatial_freq_cpp):
        nyquist_freq = 1 / (2 * self.xml.pixel_size)
        fraction_of_nyquist = (spatial_freq_cpp / 0.5)
        spatial_freq_ang = fraction_of_nyquist * nyquist_freq
        res_ang = 1 / spatial_freq_ang
        return res_ang
