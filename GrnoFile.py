import os
import codecs
import json
from Grno import Grno
from data_maps import data_keys_file


class GrnoFile:
    def __init__(self, source):
        if isinstance(source, str):
            file_data = codecs.open(source, 'r', 'utf-8')
            self.all_data = json.load(file_data)
            self.data = {k: v for k, v in self.all_data.items()
                         if k in data_keys_file}
            file_data.close()
            self.data['file_name'] = os.path.basename(source)
            if 'master' not in self.data:
                self.data['master'] = '../' + os.path.basename(source)
        if isinstance(source, Grno):
            nodes = source.paragraphs
            nodes.extend(source.segments)
            nodes.extend(source.tokens)
            nodes.extend(source.anno_nodes)
            file_edges = [edge for edge in source.edges
                          if edge['start'] not in source.indep or
                          edge['end'] not in source.indep]
            inv_edges = self.dict_to_edges_fwd(source.maps['o'], 'o')
            inv_edges.extend(self.dict_to_edges_bwd(source.maps['sp'], 'sp'))
            inv_edges.extend(self.dict_to_edges_bwd(source.maps['s'], 's'))
            inv_edges.extend(self.dict_to_edges_bwd(source.maps['p'], 'p'))
            max_edge_id = source.get_max_edge_id()
            dict_edges = [dict(edge, **{'id': i + 1 + max_edge_id})
                          for i, edge in enumerate(inv_edges)]
            self.data = {meta: source.file_meta[meta]
                         for meta in data_keys_file
                         if meta in source.file_meta}
            self.data['nodes'] = nodes
            self.data['edges'] = file_edges + dict_edges

    def dict_to_edges_bwd(self, mp, edge_type):
        edge_list = [{'type': edge_type,
                      'start': pair[1],
                      'end': pair[0]}
                     for pair in mp.items()]
        return edge_list

    def dict_to_edges_fwd(self, mp, edge_type):
        edge_list = [{'type': edge_type,
                      'start': pair[0],
                      'end': pair[1]}
                     for pair in mp.items()]
        return edge_list

    def write_to_file(self, file_name=''):
        file_dir = self.data['base_dir'] + '/' + self.data['corpus_name']
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        if file_name == '':
            file_name = file_dir + '/' + self.data['file_name']
        write_data = self.data
        json_data = json.dumps(write_data)
        write_file = codecs.open(file_name, 'w', 'utf-8')
        write_file.write(json_data)
        write_file.close()
