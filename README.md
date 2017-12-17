
# GraphPynt: A Python interface to GraphAnno

This package allows users to import, manipulate and export [GraphAnno](http://github.com/LBierkandt/graph-anno) data in a Python environment.

# Data structure

See the GraphAnno [documentation](https://github.com/LBierkandt/graph-anno/blob/master/doc/GraphAnno-Documentation_en.pdf) for information on the data model

# Corpus structure

A GraphAnno-corpus consists of documents. GraphAnno data are stored in JSON-files. A JSON-file may contain (i) all data pertaining to a corpus (mono-document corpus), (ii) only corpus-related data (-> master-file or corpus), or (iii) only the data of a document forming part of a corpus (-> document file).

GraphPynt separates corpus data and documents. Documents are represented in Grno-objects. Grno-objects are instantiated from pairs of a GrnoCorp-object (providing the corpus data) and a GrnoFile-object (providing the document data). The latter objects are instantiated from the JSON-files. GrnoCorp- and GrnoFile-objects contain the data in a way analogous to the serialization format, stored in dictionaries. A Grno-object is instantiated as follows:

corp = GrnoCorp(master.json)
file = GrnoFile(document.json)
grno = Grno(corp, file)

In the case of mono-document files:

corp = GrnoCorp(data.json)
file = GrnoFile(data.json)
grno = Grno(corp, file)

When being saved, they will be split up into a corpus file, carrying a prefix 'c_', and a document file, carrying a prefix 'f_'.

# The Grno-class

The annotation graph is represented in the form of lists of nodes and edges. Objects of class Grno have an attribute .nodes and an attribute .edges, which are dictionaries of the following form:

g.nodes = {
 'anno': [],
 'indep': [],
 'paragraph': [],
 'segment': [],
 'speaker': [],
 'token': []
 }

g.edges = {
{'anno': [],
 'order': {'anno': [],
           'segment': [],
           'token': []}}

# A typical workflow for graph manipulation:

from Grno import *  
in_corp = GrnoCorp('corp.json')
in_file = GrnoFile('document.json')
graph = Grno(in_corp, in_file)  

for segment in graph.segments:  
    do something ... (e.g. syntactic parsing, eliciting annotations in an interactive way, etc.)  

out_corp = GrnoCorp(graph)  
out_corp.write_to_file('new_corp.json')

out_file = GrnoFile(graph)
out_file.write_to_file('new_document.json')

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


