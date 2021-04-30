import networkx as nx
from siset.file import load_networkx_graph, _get_file_format
from siset.algorithms import networkx_bfs


_MAX_DEPTH = 4




def compute_graph_metrics(G):
  metrics = _get_metrics(G)
  inv = 1 / G.order()
  metrics['avg'] = [ inv * metrics['accum'][i] for i in range(_MAX_DEPTH) ]
  metrics['vertex_count'] = G.order() 
  metrics['edge_count'] = G.size()
  return metrics



def save_metrics(metrics, filename):
  file_format = _get_file_format(filename)
  overview = filename.replace(f'.{file_format}', '_metrics.csv')
  histogram = filename.replace(f'.{file_format}', '_histogram.csv')
  file = open(overview, 'wt')
  header = \
    'No. vertices,No. aristas,Diametro,Distancia,Promedio,Id Min,' + \
    'Id Max,Min 1,Min 2,Min 3,Min 4,Max 1,Max 2,Max 3,Max 4\n'
  file.write(header)
  for i in range(_MAX_DEPTH):
    if i == 0:
      file.write(
        '{},{},n/a,{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
          metrics['vertex_count'], metrics['edge_count'], i + 1, 
          metrics['avg'][i], 
          metrics['min'][i]['idx'], metrics['max'][i]['idx'],
          metrics['min'][0]['degrees'][i], metrics['min'][1]['degrees'][i],
          metrics['min'][2]['degrees'][i], metrics['min'][3]['degrees'][i],
          metrics['max'][0]['degrees'][i], metrics['max'][1]['degrees'][i],
          metrics['max'][2]['degrees'][i], metrics['max'][3]['degrees'][i]))
    else:
      file.write(
        ',,,{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
          i + 1, metrics['avg'][i], 
          metrics['min'][i]['idx'], metrics['max'][i]['idx'],
          metrics['min'][0]['degrees'][i], metrics['min'][1]['degrees'][i],
          metrics['min'][2]['degrees'][i], metrics['min'][3]['degrees'][i],
          metrics['max'][0]['degrees'][i], metrics['max'][1]['degrees'][i],
          metrics['max'][2]['degrees'][i], metrics['max'][3]['degrees'][i]))
  file.close()
  largest = 0
  for i in range(_MAX_DEPTH):
    if metrics['max'][i]['value'] > largest: 
      largest = metrics['max'][i]['value']
  file = open(histogram, 'wt')
  file.write('Cantidad,Distancia 1,Distancia 2,Distancia 3,Distancia 4\n')
  for i in range(1, largest + 1):
    line = f'{i},'
    for j in range(_MAX_DEPTH):
      if i in metrics['histograms'][j]: 
        line += '{},'.format(metrics['histograms'][j][i])
      else:
        line += '0,'
    file.write(line + '\n')
  file.close()



def _get_metrics(G):
  degrees = []
  minimums = [
    { 'idx': None, 'value': float('inf'), 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': float('inf'), 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': float('inf'), 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': float('inf'), 'degrees': _MAX_DEPTH * [ 0 ] }
  ]
  maximums = [
    { 'idx': None, 'value': 0, 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': 0, 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': 0, 'degrees': _MAX_DEPTH * [ 0 ] },
    { 'idx': None, 'value': 0, 'degrees': _MAX_DEPTH * [ 0 ] }
  ]
  accum_degrees = _MAX_DEPTH * [ 0 ]
  histograms = [ {}, {}, {}, {} ]
  for vertex in G.nodes.values():
    networkx_bfs(vertex, 4, _init, _visit, G, degrees)
    for i in range(_MAX_DEPTH):
      accum_degrees[i] += degrees[i]
      if degrees[i] < minimums[i]['value']:
        minimums[i]['idx'] = vertex['idx']
        minimums[i]['value'] = degrees[i]
        minimums[i]['degrees'] = degrees.copy()
      if degrees[i] > maximums[i]['value']:
        maximums[i]['idx'] = vertex['idx']
        maximums[i]['value'] = degrees[i]
        maximums[i]['degrees'] = degrees.copy()
      if degrees[i] in histograms[i]:
        histograms[i][degrees[i]] += 1
      else:
        histograms[i][degrees[i]] = 1
  return {
    'accum': accum_degrees,
    'min': minimums,
    'max': maximums,
    'histograms': histograms
  }



def _init(source, degrees):
  degrees[:] = [ 0, 0, 0, 0 ]



def _visit(parent, child, source, distance, G, degrees):
  degrees[distance - 1] += 1
