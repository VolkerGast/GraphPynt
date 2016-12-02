
# GraphPynt: A Python interface to GraphAnno

This package allows users to import, manipulate and export [GraphAnno](http://github.com/LBierkandt/graph-anno) data in a Python environment.

# Data structure

The data is represented as a graph. All tokens ('type': 't') and annotation nodes ('type': 'a') are assigned to one segment (type 's'). Tokens are ordered (by order edges). Segments may be assigned to paragraphs ('type': 'p'), and paragraphs may be assigned to higher-level paragraphs.

# The Grno-class

The data is represented in Grno-objects in the form of lists (nodes, annotation edges, order edges) and dictionaries (assignment edges from paragraphs, segments or speakers to nodes; a map from node-ids to nodes).

Lists of nodes:
- .paragraphs: paragraph nodes
- .segments: segment nodes
- .speakers: speaker nodes
- .tokens: token nodes
- .anno_nodes: annotation nodes

Lists of edges:
- .anno_edges: annotation edges
- .order_edges_anno: order edges between annotation nodes
- .order_edges_token: order edges between tokens
- .order_edges_segment: order edges between segments

Dictionaries/maps:
- .paragraph_map: mapping from segments or paragraphs to (higher-level) paragraphs
- .segment_map: mapping from nodes to segments
- .speaker_map: mapping from nodes to speakers

# The GrnoJson-class

Grno-objects are initialized from GrnoJson-objects, which contain the data in the form of a json-Object as represented in the native GraphAnno format.

GrnoJson-objects may be initialized from file names (str), dictionaries (dict) or Grno-objects (Grno). The class identifies the type of its argument.

A typical workflow for graph manipulation:

from .GrnoJson import GrnoJson  
indata = GrnoJson('old_file.json')  
from .Grno import Grno  
graph = Grno(indata)  

for segment in graph.segments:  
    do something ... (e.g. syntactic parsing, eliciting annotations in an interactive way, etc.)  

outdata = GrnoJson(graph)  
outdata.write_to_file('new_file.json')  

# Some functionalities (implemented though not yet on GitHub):

* import from raw text into GraphAnno, with sectioning, tagging, parsing, etc.
* import of parallel data (original and translation) from Europarl, OpenSubtitles
* import from other corpus formats, e.g.
** CoNLL-formats
** pos-tagged (e.g. SGML, XML)
** specific corpus formats such as the TimeML, LLC
** etc.
* interface to Python graph-tool
* ... and basically everything else that can be done with Python packages, e.g. those of the NLTK


