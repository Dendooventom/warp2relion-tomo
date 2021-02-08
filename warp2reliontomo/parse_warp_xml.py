from xml.dom.minidom import parse
import numpy as np


def parse_xml(node):
    """
    recursively parse an xml document node from a Warp file
    return a nested dictionary containing the node data
    """
    # node type 9 is the document node, we immediately dive deeper
    if node.nodeType == 9:
        return parse_xml(node.firstChild)

    node_name = node.localName
    node_content = {}

    if node.attributes:
        # Param nodes separate their key/value pairs as
        # different attribute tuples
        if node_name == 'Param':
            key, value = node.attributes.items()
            node_name = key[1]
            node_content = value[1]
        # Node nodes contain a xyz tuple and a value
        elif node_name == 'Node':
            x, y, z, value = node.attributes.items()
            node_name = (x[1], y[1], z[1])
            node_content = value[1]
        # everything else contains normal key/value pairs
        else:
            for attr, value in node.attributes.items():
                node_content[attr] = value
    # recursively call this function on child nodes and
    # update this node's dictionary
    if node.childNodes:
        for child in node.childNodes:
            node_content.update(parse_xml(child))
    # text nodes (type 3)
    if node.nodeType == 3:
        text = node.data.strip()
        # ignore empty text
        if not text:
            return {}
        # parse text that contains data points into np.arrays
        try:
            points = np.asarray([p.split('|') for p in text.split(';')],
                                dtype=np.float)
        except:
            points = np.array(text.split('\n'))
        node_content = points

    return {node_name: node_content}


def xml2dict(xml_path):
    """
    parse an xml metadata file of a Warp tilt-series image
    return a dictionary containing the metadata
    """
    document = parse(xml_path)
    return parse_xml(document)
