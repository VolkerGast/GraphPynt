import os
import codecs
import json
from Grno import Grno
from data_maps import data_keys_corp


class GrnoCorp:
    def __init__(self, source):
        if isinstance(source, str):
            file_data = codecs.open(source, 'r', 'utf-8')
            self.data = json.load(file_data)
            file_data.close()
            self.data['base_dir'] = os.path.dirname(source)
            self.data['corpus_file'] = os.path.basename(source)
            self.data['corpus_name'] = self.data['corpus_file'].replace(
                '.json', '')
            if 'files' not in self.data:
                self.data['files'] = [self.data['corpus_name'] + '/' +
                                      source.split('/')[-1]]
            if 'max_node_id' not in self.data:
                self.data['max_node_id'] = self.max_node_id()
            if 'max_edge_id' not in self.data:
                self.data['max_edge_id'] = self.max_edge_id()
        if isinstance(source, Grno):
            self.data = {meta: source.corp_meta[meta]
                         for meta in data_keys_corp
                         if meta in source.corp_meta}
            self.data['nodes'] = [node for node in source.speakers]
            self.data['nodes'].extend(source.indep)
            corp_file_node_ids = [node['id'] for node
                                  in self.data['nodes']]
            self.data['edges'] = [edge for edge in source.edges
                                  if edge['start'] in corp_file_node_ids and
                                  edge['end'] in corp_file_node_ids]
            self.data['max_node_id'] = source.max_node_id
            self.data['max_edge_id'] = source.max_edge_id

    def max_node_id(self):
        if self.data['nodes'] != []:
            max_id = max([node['id'] for node in self.data['nodes']])
        else:
            max_id = 0
        return max_id

    def max_edge_id(self):
        if self.data['edges'] != []:
            max_id = max([edge['id'] for edge in self.data['edges']])
        else:
            max_id = 0
        return max_id

    def write_to_file(self, file_name=''):
        if file_name == '':
            file_name = self.data['base_dir'] + '/' + self.data['corpus_file']
        json_data = json.dumps(self.data)
        write_file = codecs.open(file_name, 'w', 'utf-8')
        write_file.write(json_data)
        write_file.close()
