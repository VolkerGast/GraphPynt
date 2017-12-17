
import codecs
import json
from Grno import Grno
from data_maps import map_type_map_file
from data_maps import data_keys_file
from functions import dict_to_edge_list


class GrnoJsonFile:
    def __init__(self, source):
        if isinstance(source, str):
            file_data = codecs.open(source, 'r', 'utf-8')
            self.all_data = json.load(file_data)
            self.data = {k: v for k, v in self.all_data.items()
                         if k in data_keys_file}
            file_data.close()
            self.data['file_name'] = source
        if isinstance(source, Grno):
            dict_edge_lists = [dict_to_edge_list(source.maps[map_type],
                                                 edge_type)
                               for edge_type, map_type
                               in map_type_map_file.items()]
            dict_edges = [edge for edge_list in dict_edge_lists
                          for edge in edge_list]
            max_edge = source.get_max_edge_id()
            dict_edges = [edge.update({'id': i + max_edge})
                          for i, edge in enumerate(dict_edges)]
            self.data = {'nodes': source.all_file_nodes(),
                         'edges': source.all_file_edges() + dict_edges,
                         'version': source.version_file,
                         'master': source.master}

    def write_to_file(self, file_name=''):
        if file_name == '':
            file_name = self.data['file_name']
        if file_name[:2] != 'f_':
            file_name = 'f_' + file_name
        write_data = self.data
        json_data = json.dumps(write_data)
        write_file = codecs.open(file_name, 'w', 'utf-8')
        write_file.write(json_data)
        write_file.close()
