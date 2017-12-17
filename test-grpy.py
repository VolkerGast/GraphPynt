import json
from GrnoJsonCorp import GrnoJsonCorp
from GrnoJsonFile import GrnoJsonFile
from Grno import Grno

node_type_map_file = {
    'p': 'paragraph',
    's': 'segment',
    'a': 'anno',
    't': 'token',
    'sp': 'speaker'}

dd = '/home/volker/GraphAnno/data/'
a = GrnoJsonCorp(dd + 'template.json')
b = GrnoJsonFile(dd + 'template.json')
c = Grno(a, b)
d = GrnoJsonCorp(c)
e = GrnoJsonFile(c)

#x = {node_type: [node for node in d.data['nodes']
#                 if node['type'] == abbr]
#     for abbr, node_type in node_type_map_file.items()}
