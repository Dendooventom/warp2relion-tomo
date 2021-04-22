import click

from utils import CTFFindWriter


def warp_xml_2_cttfind(warp_xml_file):
    output_filename = str(warp_xml_file).replace('.xml', '_ctffind4_output.txt')
    CTFFindWriter(warp_xml_file).write_file(output_filename)


@click.command()
@click.option('--input', '-i', 'warp_xml_file',
              help='Warp tilt-series XML file',
              prompt='Warp tilt-series XML file',
              type=click.Path(exists=True),
              required=True)
def cli(warp_xml_file):
    warp_xml_2_cttfind(warp_xml_file)

