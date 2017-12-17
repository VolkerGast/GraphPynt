import codecs
import json
from Grno import Grno
from data_maps import data_keys_corp
from functions import get_indep_nodes


class GrnoJsonCorp:
    # Grno-data as Python dictonary
    # instatiated from a file (string)
    # or a Grno-object
    def __init__(self, source):
        if isinstance(source, str):
            file_data = codecs.open(source, 'r', 'utf-8')
            self.data = json.load(file_data)
            file_data.close()
#            self.data = {k: v for k, v in self.all_data.items()
#                         if k in data_keys_corp}
#            self.data['nodes'] = self.all_data['nodes']
#            self.data['edges'] = self.all_data['edges']
            self.data['file_name'] = source
            if 'files' not in self.data:
#                self.data['files'] = self.all_data['files']
#            else:
                self.data['files'] = [source]
            if 'max_node_id' not in self.data:
#                self.data['max_node_id'] = self.all_data['max_node_id']
#            else:
                self.data['max_node_id'] = self.max_node_id()
            if 'max_edge_id' not in self.data:
#                self.data['max_edge_id'] = self.all_data['max_edge_id']
#            else:
                self.data['max_edge_id'] = self.max_edge_id()
        if isinstance(source, Grno):
            self.data = {meta: source.meta[meta] for meta
                         in data_keys_corp if meta in source.meta}
            self.data['nodes'] = [node for node in source.nodes['speaker']]
            self.data['nodes'].extend(source.nodes['indep'])
            # master-file edges need to be implemented
            self.data['edges'] = []

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

    def dict_to_edge_list(self, data_dict, edge_type):
        edge_id = self.max_edge_id()
        edge_list = [
            {'id': i + edge_id + 1, 'type': edge_type,
             'start': pair[1], 'end': pair[0]}
            for i, pair
            in enumerate(data_dict.items())]
        return edge_list

    def add_edges_from_dict(self, data_dict, edge_type):
        new_edges = self.dict_to_edge_list(data_dict, edge_type)
        self.data['edges'] = self.data['edges'] + new_edges

    def write_to_file(self, file_name=''):
        import json
        import codecs
        if file_name == '':
            file_name = self.data['file_name']
        if 'master' not in self.data or self.data['master'] == '':
            write_data = self.data
            if 'master' in write_data:
                del write_data['master']
        else:
            write_data = {k: v for k in self.data
                          if k not in meta_data_keys}
            write_data['nodes'] = [node for node in write_data['nodes']
                                   if type['node'] != 'sp']
        json_data = json.dumps(write_data)
        write_file = codecs.open(file_name, 'w', 'utf-8')
        write_file.write(json_data)
        write_file.close()
        
