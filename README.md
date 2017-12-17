
# GraphPynt: A Python interface to GraphAnno

This package allows users to import, manipulate and export [GraphAnno](http://github.com/LBierkandt/graph-anno) data in a Python environment.

# Data structure

See the [documentation](https://github.com/LBierkandt/graph-anno/blob/master/doc/GraphAnno-Documentation_en.pdf) for information on the data model

# Corpus structure

A GraphAnno-corpus consists of documents. GraphAnno data are stored in JSON-files. A JSON-file may contain (i) all data pertaining to a corpus (mono-document corpus), (ii) only corpus-related data (-> master-file or corpus), or (iii) only the data of a document forming part of a corpus (-> document file).

GraphPynt separates corpus data and documents. Documents are represented in Grno-objects. Grno-objects are instantiated from pairs of a GrnoCorp-object (providing the corpus data) and a GrnoFile-object (providing the document data). The latter objects are instantiated from the JSON-files. GrnoCorp- and GrnoFile-objects contain the data in a way analogous to the serialization format, stored in dictionaries.

master.json -> GrnoCorp(master.json)
                                            \
                                              Grno(GrnoCorp(master.json), GrnoFile(document.json))
			                    /
document.json -> GrnoFile(document.json)

In the case of mono-document files, both the GrnoJsonCorp and the GrnoJsonFile are instantiated from the same JSON-file. When being saved, they will be split up into a corpus file, carrying a prefix 'c_', and a document file, carrying a prefix 'f_'.

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

from .GrnoJson import *  
in_data = GrnoJson('old_file.json')  
graph = Grno(in_data)  

for segment in graph.segments:  
    do something ... (e.g. syntactic parsing, eliciting annotations in an interactive way, etc.)  

out_data = GrnoJson(graph)  
out_data.write_to_file('new_file.json')  

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


