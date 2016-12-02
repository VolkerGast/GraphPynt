class Grno:
    def __init__(self, json_data):
        # invisible nodes
        self.paragraphs = [node for node in json_data.data['nodes']
                           if node['type'] == 'p']
        self.segments = [node for node in json_data.data['nodes']
                         if node['type'] == 's']
        self.speakers = [node for node in json_data.data['nodes']
                         if node['type'] == 'sp']
        # visible nodes
        self.tokens = [node for node
                       in json_data.data['nodes']
                       if node['type'] == 't']
        self.anno_nodes = [node for node
                           in json_data.data['nodes']
                           if node['type'] == 'a']
        # map from node ids to nodes
        self.node_map = {node['id']: node for node
                         in json_data.data['nodes']}
        # visible edges
        self.anno_edges = [edge for edge
                           in json_data.data['edges']
                           if edge['type'] == 'a']
        # order edges (invisible)
        self.order_edges_anno = [edge for edge
                                in json_data.data['edges']
                                if edge['type'] == 'o'
                                and
                                self.node_map[edge['start']]['type'] == 'a']
        self.order_edges_token = [edge for edge
                                in json_data.data['edges']
                                if edge['type'] == 'o'
                                and
                                self.node_map[edge['start']]['type'] == 't']
        self.order_edges_segment = [edge for edge
                                in json_data.data['edges']
                                if edge['type'] == 'o'
                                and
                                self.node_map[edge['start']]['type'] == 's']
        # maps
        self.paragraph_map = {edge['end']: edge['start'] for edge
                              in json_data.data['edges']
                              if edge['type'] == 'p'}
        self.segment_map = {edge['end']: edge['start'] for edge
                            in json_data.data['edges']
                            if edge['type'] == 's'}
        self.speaker_map = {edge['end']: edge['start'] for edge
                            in json_data.data['edges']
                            if edge['type'] == 'sp'}
        # metadata
        self.version = json_data.data['version']
        self.info = json_data.data['info']
        self.anno_makros = json_data.data['anno_makros']
        self.tagset = json_data.data['tagset']
        self.annotators = json_data.data['annotators']
        self.file_settings = json_data.data['file_settings']
        self.search_makros = json_data.data['search_makros']
        self.conf = json_data.data['conf']

    # graph manipulation
    # create nodes
    def create_paragraph(self, attr, nodeid):
        '''takes attribute-dictionary and nodeid and returns nodeid'''
        nodeid += 1
        node = {'id': nodeid, 'type': 'p', 'attr': attr}
        self.paragraphs.append(node)
        return nodeid

    def create_segment(self,attr,nodeid):
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
        nodeid +=1
        self.tokens.append({'id': nodeid, 'type':'t', 'attr': attr,
                            'start': start, 'end': end})
        self.segment_map[nodeid] = sentid
        self.speaker_map[nodeid] = spkid
        return nodeid

    def create_anno_node(self, sentid, attr, nodeid):
        '''takes segment-id, attribute-dict and nodeid
        and returns nodeid
        '''
        nodeid +=1
        node = {'id': nodeid, 'type': 'a', 'attr': attr}
        self.anno_nodes.append(node)
        self.segment_map[nodeid] = sentid
        return nodeid

    def create_anno_edge(self, start, end, attr, edgeid):
        '''takes start-node, end-node, attribute-dict and edgeid
        and returns edgeid
        '''
        edgeid +=1
        edge = {'type': 'a', 'start': start, 'end': end, 'attr': attr}
        self.anno_edges.append(edge)
        return edgeid
        
    def create_parent(self, sentid, childids, nodeattr, edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of child-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a nodeid and an edgeid
        and returns nodeid, edgeid
        '''
        nodeid = self.create_anode(sentid, nodeattr, nodeid)
        for childid in childids:
            edgeid = self.create_aedge(nodeid, childid, edgeattr, edgeid)
        return nodeid, edgeid

    def create_child(self, sentid, motherids, nodeattr, edgeattr, nodeid, edgeid):
        '''takes segment-id, a list of mother-ids, an attribute-dict for the nodes,
        an attribute-dict for the edges, a noreid and an edgeid
        and returns nodeid, edgeid'''
        nodeid = self.create_anode(sentid, nodeattr, nodeid)
        for motherid in motherids:
            edgeid = self.create_aedge(motherid, nodeid, edgeattr, edgeid)
        return nodeid, edgeid


    # create order edges ...
    # ... between tokens
    def create_order_edge_token(self, start, end, edgeid):
        '''takes start node, end node and edgeid
        and returns edgeid
        '''
        self.order_edges_token.append({'type': 'o', 'start': start, 'end': end})
        return edgeid

    def create_order_edges_token(self, tokens, sortkey, edgeid):
        '''takes list of tokens, sortkey and edgeid
        and returns edgeid
        '''
        for i, token in enumerate(sorted(tokens[:-1], key = lambda x: x[sortkey])):
            edgeid += 1
            self.create_order_edge_token(token['id'], tokens[i+1], edgeid)
        return edgeid

    # ... between annotation nodes of a specific level
    def create_order_edge_anno(self, start, end, edgeid):
        '''takes start-node-id, end-node-id and returns edgeid'''
        self.order_edges_anno.append({'id': edgeid, 'type':'o',
                                      'start': start, 'end': end})
        return edgeid

    def create_order_edges_anno(self, anno_nodes, sortkey, edgeid):
        '''takes list of anno-nodes, sortkey and edgeid
        and returns edgeid'''
        for i, anode in enumerate(sorted(anno_nodes[:-1], key = lambda x: x[sortkey])):
            edgeid += 1
            self.create_order_edge_anno(anode['id'], anode[i+1], edgeid)
        return edgeid
    
    # ... between segments
    def create_order_edge_segment(self, start, end, edgeid):
        '''takes start-segment-id and end-segment-id
        and returns edgeid'''
        self.order_edges_segment.append({'type': 'o', 'start': start, 'end': end})
        return edgeid

    def create_order_edges_seg(self, segments, sortkey, edgeid):
        '''takes list of segments, sortkey and edgeid
        and returns edgeid'''
        for i, segment in enumerate(sorted(segments[:-1], key = lambda x: x[sortkey])):
            edgeid += 1
            self.create_order_edge_segment(segment['id'], segment[i+1], edgeid)
        return edgeid
    
    # associating tokens and segments
    def get_segment_tokens(self, sentid, sortkey='start'):
        '''takes segment-id and sortkey
        and returns list of tokens
        '''
        tokens = sorted([node for node in self.tokens
                         if self.segment_map[node['id']] == sentid],
                        key = lambda x: x[sortkey])
        return tokens

    def order_tokens_by_order_edges(self, sentid):
        '''takes segment-id
        and returns token list ordered according to order edges
        '''
        token_ids = [token['id'] for token in self.get_seg_tokens(sentid)]
        order_edges_segment = [edge for edge in self.order_edges_token
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


