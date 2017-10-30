from .functions import node_type_map
from .functions import meta_data_keys

class Grno:
    # Grno-objects are instantiated from GrnoJson-objects
    def __init__(self, json_data):
        if 'master' in json_data.data:
            self.data_type = 'corpus_part'
            master_data = self.get_master_data(json_data.data['file_name'], json_data.data['master'])
        else:
            self.data_type = 'corpus'
        self.node_map = {node['id']: node for node
                         in json_data.data['nodes']}
        # lists of nodes
        self.nodes = {node_type: [] for node_type
                      in list(node_type_map.values())}
        for node in json_data.data['nodes']:
            self.nodes[node_type_map[node['type']]].append(node)

        if self.data_type == 'corpus_part':
            if 'nodes' in master_data.data:
                self.nodes['speakers'] = [
                    node for node in master_data.data['nodes']]
            else:
                self.nodes['speakers'] = []

        self.edges = {'anno': [],
                      'order': {'token': [], 'anno': [], 'segment': []}}
        for edge in json_data.data['edges']:
            if edge['type'] == 'o':
                node_type = self.node_map[edge['start']]['type']
                self.edges['order'][node_type_map[node_type]].append(edge)
            if edge['type'] == 'a':
                self.edges['anno'].append(edge)
        # maps from invisible nodes to visible nodes
        self.maps = {}
        self.maps['paragraph'] = self.convert_edges_to_dict('p', json_data.data['edges'])
        self.maps['segment'] = self.convert_edges_to_dict('s', json_data.data['edges'])
        self.maps['speaker'] = self.convert_edges_to_dict('sp', json_data.data['edges'])
        if self.data_type == 'corpus':
            self.meta = {meta: json_data.data[meta]
                         for meta in meta_data_keys
                         if meta in json_data.data}
        if self.data_type == 'corpus_part':
            self.meta = {meta: master_data.data[meta]
                         for meta in meta_data_keys
                         if meta in master_data.data}
            #self.files = master_data.data['files']
            #self.max_node_id = master_data.data['max_node_id']
            #self.max_edge_id = master_data.data['max_edge_id']

    def all_nodes(self):
        from .functions import node_type_map
        all_nodes = [
            node for node_type in node_type_map.values()
            for node in self.nodes[node_type]]
        return all_nodes

    def all_edges(self):
        from .functions import node_type_map
        order_edges = [edge for node_type in node_type_map.values()
                       if node_type in self.edges['order']
                       for edge in self.edges['order'][node_type]]
        all_edges = self.edges['anno'] + order_edges
        return all_edges

    def max_node_id(self):
        if self.all_nodes() != []:
            max_id = max([node['id'] for node in self.all_nodes()])
        else:
            max_id = 0
        return max_id

    def max_edge_id(self):
        if self.all_edges() != []:
            max_id = max([edge['id'] for edge in self.all_edges()])
        else:
            max_id = 0
        return max_id

    def convert_edges_to_dict(self, edge_type, edge_list):
        new_dict = {edge['end']: edge['start'] for edge
                    in edge_list if edge['type'] == edge_type}
        return new_dict
    
    def get_master_data(self, file_name, master_file_name):
        from .GrnoJson import GrnoJson
        file_path = '/'+'/'.join(file_name.split('/')[:-1])+'/'
        master_file = file_path+master_file_name
        return GrnoJson(master_file)

        
    # graph manipulation
    # create nodes
    def create_paragraph(self, attr, nodeid):
        '''takes attribute-dictionary and nodeid and returns nodeid'''
        nodeid += 1
        node = {'id': nodeid, 'type': 'p', 'attr': attr}
        self.nodes['paragraph'].append(node)
        return nodeid

    def create_segment(self,attr,nodeid):
        '''takes attribute-dictionary and nodeid and returns nodeid'''
        nodeid += 1
        node = {'id': nodeid, 'type': 's', 'attr': attr}
        self.nodes['segment'].append(node)
        return nodeid

    def create_token(self, sentid, spkid, attr, start, end, nodeid):
        '''takes segment-id, speaker-id, attribute-dict, 
        start-index, end-index and nodeid
        and returns nodeid
        '''
        nodeid +=1
        self.nodes['token'].append({'id': nodeid, 'type':'t', 'attr': attr,
                            'start': start, 'end': end})
        self.maps['segment'][nodeid] = sentid
        self.maps['speaker'][nodeid] = spkid
        return nodeid

    def create_anno_node(self, sentid, attr, layers, nodeid):
        '''takes segment-id, attribute-dict and nodeid
        and returns nodeid
        '''
        nodeid +=1
        node = {'id': nodeid, 'type': 'a', 'attr': attr, 'layers': layers}
        self.nodes['anno'].append(node)
        self.maps['segment'][nodeid] = sentid
        return nodeid

    def create_anno_edge(self, start, end, attr, layers, edgeid):
        '''takes start-node, end-node, attribute-dict and edgeid
        and returns edgeid
        '''
        edgeid +=1
        edge = {'type': 'a', 'start': start, 'end': end,
                'attr': attr, 'layers': layers, 'id': edgeid}
        self.edges['anno'].append(edge)
        return edgeid
        
    def create_parent(self, sentid, childids, nodeattr, edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of child-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a nodeid and an edgeid
        and returns nodeid, edgeid
        '''
        nodeid = self.create_anno_node(sentid, nodeattr, nodeid)
        for childid in childids:
            edgeid = self.create_anno_edge(nodeid, childid, edgeattr, edgeid)
        return nodeid, edgeid

    def create_child(self, sentid, motherids, nodeattr, edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of mother-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a noreid and an edgeid
        and returns nodeid, edgeid'''
        nodeid = self.create_anno_node(sentid, nodeattr, nodeid)
        for motherid in motherids:
            edgeid = self.create_anno_edge(motherid, nodeid, edgeattr, edgeid)
        return nodeid, edgeid

    # create order edges ...
    # ... between tokens
    def create_order_edge_token(self, start, end, edgeid):
        '''takes start node, end node and edgeid
        and returns edgeid
        '''
        edgeid += 1
        self.edges['order']['token'].append({'type': 'o', 'start': start, 'end': end, 'id': edgeid})
        return edgeid

    def create_order_edges_token(self, tokens, sortkey, edgeid):
        '''takes list of tokens, sortkey and edgeid
        and returns edgeid
        '''
        for i, token in enumerate(sorted(tokens[:-1], key = lambda x: x[sortkey])):
            self.create_order_edge_token(token['id'], tokens[i+1]['id'], edgeid)
        return edgeid

    # ... between annotation nodes of a specific level
    def create_order_edge_anno(self, start, end, edgeid):
        '''takes start-node-id, end-node-id and returns edgeid'''
        edgeid += 1
        self.order_edges_anno.append({'id': edgeid, 'type':'o',
                                      'start': start, 'end': end})
        return edgeid

    def create_order_edges_anno(self, anno_nodes, sortkey, edgeid):
        '''takes list of anno-nodes, sortkey and edgeid
        and returns edgeid'''
        sort_nodes = sorted(anno_nodes, key = lambda x: x[sortkey])
        for i, anode in enumerate(sort_nodes[:-1]):
            self.create_order_edge_anno(anode['id'], sort_nodes[i+1]['id'], edgeid)
        return edgeid
    
    # ... between segments
    def create_order_edge_segment(self, start, end, edgeid):
        '''takes start-segment-id and end-segment-id
        and returns edgeid'''
        edgeid += 1
        self.edges['order']['segment'].append({'type': 'o', 'start': start, 'end': end, 'id': edgeid})
        return edgeid

    def create_order_edges_segment(self, segments, sortkey, edgeid):
        '''takes list of segments, sortkey and edgeid
        and returns edgeid'''
        for i, segment in enumerate(sorted(segments[:-1], key = lambda x: x[sortkey])):
            self.create_order_edge_segment(segment['id'], segments[i+1]['id'], edgeid)
        return edgeid
    
    # associating tokens and segments
    def get_segment_tokens(self, sentid, sortkey='start'):
        '''takes segment-id and sortkey
        and returns list of tokens
        '''
        tokens = sorted([node for node in self.nodes['token']
                         if self.maps['segment'][node['id']] == sentid],
                        key = lambda x: x[sortkey])
        return tokens

    # associating tokens and segments
    def get_segment_nodes_anno(self, sentid, sortkey='start'):
        '''takes segment-id and sortkey
        and returns list of tokens
        '''
        tokens = sorted([node for node in self.nodes['anno']
                         if self.maps['segment'][node['id']] == sentid],
                        key = lambda x: x[sortkey])
        return tokens

    
    def order_tokens_by_order_edges(self, sentid, sortkey):
        '''takes segment-id
        and returns token list ordered according to order edges
        '''
        token_ids = [token['id'] for token in self.get_segment_tokens(sentid, sortkey)]
        order_edges_segment = [edge for edge in self.edges['order']['token']
                               if edge['start'] in token_ids
                               or edge['end'] in token_ids]
        ends = [edge['end'] for edge in order_edges_segment]
        order_edges_ord = [edge for edge in order_edges_segment
                           if edge['start'] not in ends]
        while len(order_edges_ord) < len(order_edges_segment):
            order_edges_ord.append([edge for edge in order_edges_segment
                                    if edge['start'] == order_edges_ord[-1]['end']][0])
        token_list = [self.node_map[edge['start']] for edge
                      in order_edges_ord] + [self.node_map[order_edges_ord[-1]['end']]]
        return token_list


