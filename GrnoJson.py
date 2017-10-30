from .Grno import Grno
from .functions import meta_data_keys
from .functions import map_type_map

class GrnoJson:
    # Grno-data as Python adictionary
    # instatiated from a file (string)
    # or a Grno-object
    def __init__(self, source):
        if isinstance(source, str):
            import codecs
            import json
            file_data = codecs.open(source, 'r', 'utf-8')
            self.data = json.load(file_data)
            file_data.close()
            self.data['file_name'] = source
        if isinstance(source, Grno):
            self.data = {meta: source.meta[meta] for meta
                         in meta_data_keys if meta in source.meta}
            self.data.update({
                'nodes': source.all_nodes(),
                'edges': source.all_edges()})
            for edge_type, map_type in map_type_map.items():
                self.add_edges_from_dict(source.maps[map_type], edge_type)

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

    def convert_dict_to_edge_list(self, data_dict, edge_type):
        edge_id = self.max_edge_id()
        edge_list = [
            {'id': i + edge_id + 1, 'type': edge_type,
             'start': pair[1], 'end': pair[0]}
            for i, pair
            in enumerate(data_dict.items())]
        return edge_list

    def add_edges_from_dict(self, data_dict, edge_type):
        self.data['edges'] = self.data['edges'] + self.convert_dict_to_edge_list(data_dict, edge_type)
    
    def write_to_file(self, file_name=''):
        import json
        import codecs
        if file_name == '':
            file_name = self.data['file_name']
        if not 'master' in self.data or self.data['master'] == '':
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
        
