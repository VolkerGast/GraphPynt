

# convert dictionary to list of edges
def dict_to_edge_list(data_dict, edge_type):
    edge_list = [{'type': edge_type,
                  'start': pair[1],
                  'end': pair[0]}
                 for i, pair
                 in enumerate(data_dict.items())]
    return edge_list


# get independent nodes
def get_indep_nodes(nodes, edges):
    edge_ends_s = [edge['end'] for edge in edges
                   if edge['type'] == 's']
    indep_nodes = [node for node in nodes
                   if node['type'] == 'a'
                   and node['id'] not in edge_ends_s]
    return indep_nodes
