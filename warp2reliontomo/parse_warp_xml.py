import numpy as np


def parse_xml_node(node):
    """
    recursively parse an xml document node from a Warp file
    return a nested dictionary containing the node data
    """
    # node type 9 is the document node, we immediately dive deeper
    if node.nodeType == 9:
        return parse_xml_node(node.firstChild)

    node_name = node.localName
    node_content = {}

    # node type 3 is the text node
    if node.nodeType == 3:
        node_content = parse_text_node(node)

    if node.attributes:
        if node_name == 'Param':
            node_name, node_content = parse_param_node(node)
        elif node_name == 'Node':
            node_name, node_content = parse_node_node(node)
        else:
            node_content.update(parse_basic_node(node))

    if node.childNodes:
        for child in node.childNodes:
            node_content.update(parse_xml_node(child))

    return {node_name: node_content}


def parse_param_node(node):
    """Param nodes separate their key/value pairs as different attribute tuples
    """
    key, value = node.attributes.items()
    node_name = key[1]
    node_content = value[1]
    return node_name, node_content


def parse_node_node(node):
    """Node nodes contain a xyz tuple and a value or xyzw tuple and a value
    """
    node_items = node.attributes.items()
    if len(node_items) == 4:
        x, y, z, value = node_items
        node_name = (x[1], y[1], z[1])
    elif len(node_items) == 5:
        x, y, z, w, value = node_items
        node_name = (x[1], y[1], z[1], w[1])
    node_content = value[1]
    return node_name, node_content


def parse_basic_node(node):
    node_content = {k: v for k, v in node.attributes.items()}
    return node_content


def parse_text_node(node):
    """Text nodes contain arrays of data, sometimes with weird separators...
    """
    text = node.data.strip()
    if not text:
        return {}
    # parse text that contains data points into np.arrays
    try:
        data = [d.split('|') for d in text.split(';')]
        node_content = np.array(data, dtype=float)
    except:
        data = text.split('\n')
        node_content = np.array(data)
    return node_content
