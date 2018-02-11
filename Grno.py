from data_maps import node_types
from data_maps import data_keys_corp
from data_maps import meta_keys_file


class Grno:
    # Grno-objects are instantiated from pairs of
    # GrnoCorp and GrnoFile-objects
    def __init__(self, json_corp, json_file):
        # get meta data from GrnoCorp-object
        self.corp_meta = {k: v for k, v in json_corp.data.items()
                          if k in data_keys_corp}
        self.max_node_id = json_corp.data['max_node_id']
        self.max_edge_id = json_corp.data['max_edge_id']
        self.files = json_corp.data['files']
        # get meta data from GrnoFile-object
        self.file_meta = {k: v for k, v in json_file.data.items()
                          if k in meta_keys_file}
        self.file_meta['base_dir'] = json_corp.data['base_dir']
        self.file_meta['corpus_name'] = json_corp.data['corpus_name']
        # get nodes and create node map
        self.node_map = {node['id']: node for node
                         in json_corp.data['nodes'] + json_file.data['nodes']}
        # get edges and create edge_map
        input_edges = json_corp.data['edges'] + json_file.data['edges']
        self.edge_map = {edge['id']: edge
                         for edge in input_edges
                         if edge['type'] == 'a'}
        # transform invisible edges into dicts
        self.edges = list(self.edge_map.values())
        inv_edges = [edge for edge in input_edges
                     if edge['id'] not in self.edge_map]
        self.maps = {'p': self.edges_to_dict_bwd('p', inv_edges),
                     's': self.edges_to_dict_bwd('s', inv_edges),
                     'sp': self.edges_to_dict_bwd('sp', inv_edges),
                     'o': self.edges_to_dict_fwd('o', inv_edges)}
        # identify independent nodes
        indep_node_ids = [node['id']
                          for node in self.node_map.values()
                          if node['type'] == 'a' and
                          node['id'] not in self.maps['s']]
        #indep_node_ids = self.get_indep_node_ids()
        # get nodes from GrnoFile-object
        self.nodes = {node_type: [node for node
                                  in self.node_map.values()
                                  if node['type'] == node_type and
                                  node['id'] not in indep_node_ids]
                      for node_type in node_types}
        self.segments = self.nodes['s']
        self.paragraphs = self.nodes['p']
        self.speakers = self.nodes['sp']
        self.tokens = self.nodes['t']
        self.anno_nodes = self.nodes['a']
        self.indep = [self.node_map[node_id]
                      for node_id in indep_node_ids]

    def get_max_node_id(self):
        if self.all_nodes() != []:
            max_id = max([node['id'] for node in self.all_nodes()])
        else:
            max_id = 0
        return max_id

    def get_max_edge_id(self):
        if self.edges != []:
            max_id = max([edge['id'] for edge in self.edges])
        else:
            max_id = 0
        return max_id

    def edges_to_dict_bwd(self, edge_type, edge_list):
        new_dict = {edge['end']: edge['start'] for edge
                    in edge_list if edge['type'] == edge_type}
        return new_dict

    def edges_to_dict_fwd(self, edge_type, edge_list):
        new_dict = {edge['start']: edge['end'] for edge
                    in edge_list if edge['type'] == edge_type}
        return new_dict
   
    # graph manipulation
    # create nodes
    def create_paragraph(self, attr, nodeid):
        '''takes attribute-dictionary and nodeid and returns nodeid'''
        nodeid += 1
        node = {'id': nodeid, 'type': 'p', 'attr': attr}
        self.paragraphs.append(node)
        return nodeid

    def create_segment(self, attr, nodeid):
        '''takes attribute-dictionary and nodeid and returns nodeid'''
        nodeid += 1
        node = {'id': nodeid, 'type': 's', 'attr': attr}
        self.segments.append(node)
        return nodeid

    def create_token(self, sentid, spkid, attr, start, end, nodeid):
        '''takes segment-id, speaker-id, attribute-dict,
        start-index, end-index and nodeid
        and returns nodeid
        '''
        nodeid += 1
        self.tokens.append({'id': nodeid, 'type': 't', 'attr': attr,
                            'start': start, 'end': end})
        self.maps['s'][nodeid] = sentid
        self.maps['sp'][nodeid] = spkid
        return nodeid

    def create_anno_node(self, sentid, attr, layers, nodeid):
        '''takes segment-id, attribute-dict and nodeid
        and returns nodeid
        '''
        nodeid += 1
        node = {'id': nodeid, 'type': 'a', 'attr': attr, 'layers': layers}
        self.anno_nodes.append(node)
        self.maps['s'][nodeid] = sentid
        return nodeid

    def create_edge(self, start, end, attr, layers, edgeid):
        '''takes start-node, end-node, attribute-dict and edgeid
        and returns edgeid
        '''
        edgeid += 1
        edge = {'type': 'a', 'start': start, 'end': end,
                'attr': attr, 'layers': layers, 'id': edgeid}
        self.edges.append(edge)
        return edgeid

    def create_parent(self, sentid, childids,
                      nodeattr, edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of child-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a nodeid and an edgeid
        and returns nodeid, edgeid
        '''
        nodeid = self.create_anno_node(sentid, nodeattr, nodeid)
        for childid in childids:
            edgeid = self.create_edge(nodeid, childid, edgeattr, edgeid)
        return nodeid, edgeid

    def create_child(self, sentid, motherids, nodeattr,
                     edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of mother-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a noreid and an edgeid
        and returns nodeid, edgeid'''
        nodeid = self.create_anno_node(sentid, nodeattr, nodeid)
        for motherid in motherids:
            edgeid = self.create_edge(motherid, nodeid, edgeattr, edgeid)
        return nodeid, edgeid

    # create order edges ...
    # ... between tokens
    def create_order_edge_token(self, start, end, edgeid):
        '''takes start node, end node and edgeid
        and returns edgeid
        '''
        edgeid += 1
        self.maps['o'][start] = end
        return edgeid

    def create_order_edges_token(self, tokens, sortkey, edgeid):
        '''takes list of tokens, sortkey and edgeid
        and returns edgeid
        '''
        for i, token in enumerate(sorted(tokens[:-1],
                                         key=lambda x: x[sortkey])):
            self.create_order_edge_token(token['id'],
                                         tokens[i+1]['id'], edgeid)
        return edgeid

    # ... between annotation nodes of a specific level
    def create_order_edge_anno(self, start, end, edgeid):
        '''takes start-node-id, end-node-id and returns edgeid'''
        edgeid += 1
        self.maps['o'][start] = end
        #self.order_edges_anno.append({'id': edgeid, 'type': 'o',
        #                              'start': start, 'end': end})
        return edgeid

    def create_order_edges_anno(self, anno_nodes, sortkey, edgeid):
        '''takes list of anno-nodes, sortkey and edgeid
        and returns edgeid'''
        sort_nodes = sorted(anno_nodes, key=lambda x: x[sortkey])
        for i, anode in enumerate(sort_nodes[:-1]):
            self.create_order_edge_anno(anode['id'],
                                        sort_nodes[i+1]['id'], edgeid)
        return edgeid

    # ... between segments
    def create_order_edge_segment(self, start, end, edgeid):
        '''takes start-segment-id and end-segment-id
        and returns edgeid'''
        edgeid += 1
        self.maps['o'][start] = end
        #self.edges['order']['segment'].append({'type': 'o', 'start': start,
        #                                       'end': end, 'id': edgeid})
        return edgeid

    def create_order_edges_segment(self, segments, sortkey, edgeid):
        '''takes list of segments, sortkey and edgeid
        and returns edgeid'''
        for i, segment in enumerate(sorted(segments[:-1],
                                           key=lambda x: x[sortkey])):
            self.create_order_edge_segment(segment['id'],
                                           segments[i+1]['id'], edgeid)
        return edgeid

    # associating tokens and segments
    def get_segment_tokens(self, sentid, sortkey='start'):
        '''takes segment-id and sortkey
        and returns list of tokens
        '''
        tokens = sorted([node for node in self.tokens
                         if self.maps['s'][node['id']] == sentid],
                        key=lambda x: x[sortkey])
        return tokens

    # associating tokens and segments
    def get_segment_nodes_anno(self, sentid, sortkey='start'):
        '''takes segment-id and sortkey
        and returns list of tokens
        '''
        tokens = sorted([node for node in self.anno_nodes
                         if self.maps['s'][node['id']] == sentid],
                        key=lambda x: x[sortkey])
        return tokens
