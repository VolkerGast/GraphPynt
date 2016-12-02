class GrnoJson:
    def __init__(self, source):
        if isinstance(source, str):
            import codecs
            import json
            file_data = codecs.open(source, 'r', 'utf-8')
            self.data = json.load(file_data)
            file_data.close()
        if isinstance(source, dict):
            self.data = data
        else:
            from .Grno import Grno
            if isinstance(source, Grno):
                edge_id = max([edge['id'] for edge
                              in source.anno_edges
                              + source.order_edges_token
                              + source.order_edges_anno
                              + source.order_edges_segment])
                segment_edges = [{'id': i + edge_id + 1, 'type': 's',
                                  'start': pair[1], 'end': pair[0]}
                                 for i, pair
                                 in enumerate(source.segment_map.items())]
                edge_id = max([edge['id'] for edge
                              in source.anno_edges
                              + source.oorder_edges_token
                              + source.order_edges_anno
                              + source.order_edges_segment
                              + segment_edges])
                paragraph_edges = [{'id': i + edge_id + 1, 'type': 'p',
                                    'start': pair[1], 'end': pair[0]}
                                   for i, pair
                                   in enumerate(source.paragraph_map.items())]
                edge_id = max([edge['id'] for edge
                              in source.anno_edges
                              + source.order_edges_token
                              + source.order_edges_anno
                              + source.order_edges_segment
                              + segment_edges
                              + paragraph_edges])
                speaker_edges = [{'id': i + edge_id + 1, 'type': 'sp',
                                  'start': pair[1], 'end': pair[0]}
                                 for i, pair
                                 in enumerate(source.speaker_map.items())]
                self.data = {
                    'nodes': source.paragraphs
                        + source.segments
                        + source.seakers
                        + source.tokens
                        + source.anno_nodes,
                    'info': source.info,
                    'edges': source.anno_edges
                        + segment_edges
                        + speaker_edges
                        + paragraph_edges
                        + source.order_edges_token
                        + source.order_edges_segment
                        + source.order_edges_anno,
                    'version': source.version,
                    'anno_makros': source.anno_makros,
                    'conf': source.conf,
                    'search_makros': source.search_makros,
                    'file_settings': source.file_settings,
                    'annotators': source.annotators,
                    'tagset': source.tagset
                }

    def write_to_file(self, file_name):
        import json
        import codecs
        json_data = json.dumps(self.data)
        write_file = codecs.open(file_name, 'w', 'utf-8')
        write_file.write(json_data)
        write_file.close()

    # transform strings to integers
    # needed for older versions of GraphAnno, where string ids were used
    def string_to_int(self):
        for node in self.data['nodes']:
            node['id'] = int(node['id'])
        for edge in self.data['edges']:
            edge['start'] = int(edge['start'])
            edge['end'] = int(edge['end'])
            edge['id'] = int(edge['id'])
