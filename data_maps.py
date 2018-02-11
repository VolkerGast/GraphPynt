
node_types = {
    'a',
    'p',
    's',
    'sp',
    't'}

node_type_map = {
    'p': 'paragraph',
    's': 'segment',
    'a': 'anno',
    't': 'token',
    'sp': 'speaker'}

edge_type_map_file = {
    'a': 'anno',
    'o': 'order'}

edge_type_map_edge = {
    'a': 'anno',
    'o': 'order'}

edge_type_map_dict = {
    's': 'segment',
    'p': 'paragraph',
    'sp': 'speaker'}

map_type_map_file = {
    's': 'segment',
    'p': 'paragraph',
    'sp': 'speaker',
    'o': 'order'}

map_type_map_corp = {
    'p': 'paragraph',
    'sp': 'speaker'}

# should be renamed to meta_data_keys
data_keys_corp = {
    'version',
    'conf',
    'file_name',
    'files',
    'info',
    'anno_makros',
    'search_makros',
    'file_settings',
    'annotators',
    'tagset',
    'base_dir',
    'corpus_name',
    'corpus_file',
    'corpus_dir'}

data_keys_file = {
    'nodes',
    'edges',
    'media',
    'version',
    'master',
    'base_dir',
    'corpus_name',
    'file_name'}

meta_keys_file = {
    'media',
    'version',
    'master',
    'base_dir',
    'corpus_name',
    'file_name'}

