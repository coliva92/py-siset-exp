from siset.converters import to_siset_graph, to_networkx_graph
from siset.file import load_networkx_graph
from siset.heuristics import greedy_heuristic
from experiments.metrics import compute_graph_metrics, save_metrics
import networkx as nx
import networkx.generators.random_graphs as rg
from time import perf_counter
from os import mkdir
from os.path import isdir




class IScriptsContainer:

  def __init__(self, graph_name, num_graphs):
    self._graph_name = graph_name
    self._num_graphs = num_graphs


  def _h(self, path):
    return f'{self._graph_name}\\{path}'


  def _generate_graph(self, n):
    return None


  def create_batch(self):
    if not isdir(self._graph_name): mkdir(self._graph_name)
    for i in range(11, 18, 2):
      n = 2**i
      for j in range(1, self._num_graphs+1):
        G = self._generate_graph(n)
        print(G.order(), G.size())
        graph = to_siset_graph(G)
        del G
        graph.shuffle()
        graph.relabel()
        G = to_networkx_graph(graph)
        del graph
        if j < 10: j = f'0{j}'
        nx.write_gml(G, self._h(f'{self._graph_name}_{n}_{j}.gml'))
        del G


  def compute_metrics(self):
    header = \
      'Grafo,Vertices,Aristas,Grado prom,Grado max,Vec ext prom,Vec ext max\n'
    with open(self._h('metrics.csv'), 'wt') as file: file.write(header)
    for i in range(11, 18, 2):
      n = 2**i
      filename = self._h(f'{self._graph_name}_{n}_01.gml')
      G = load_networkx_graph(filename) 
      metrics = compute_graph_metrics(G)
      del G
      with open(self._h('metrics.csv'), 'at') as file:
        file.write('{},{},{},{},{},{},{}\n'.format(
          filename, metrics['vertex_count'], metrics['edge_count'], 
          metrics['avg'][0], metrics['max'][0]['degrees'][0],
          metrics['avg'][1], metrics['max'][1]['degrees'][1]))
      save_metrics(metrics, filename)


  def compute_diameter(self):
    with open(self._h('diameters.csv'), 'wt') as file: 
      file.write('Grafo,Conectado,Diametro\n')
    for i in range(11, 16, 2):
      n = 2**i
      filename = self._h(f'{self._graph_name}_{n}_01.gml')
      G = nx.read_gml(filename)
      con = nx.is_connected(G)
      d = nx.diameter(G) if con else 'Infinito'
      del G
      with open(self._h('diameters.csv'), 'at') as file:
        file.write(f'{filename},{con},{d}\n')


  def compute_packing(self):
    with open(self._h('results.csv'), 'wt') as file: 
      file.write('Grafo,CIF,Tiempo\n')
    for i in range(11, 18, 2):
      n = 2**i
      filename = self._h(f'{self._graph_name}_{n}_01.gml')
      G = load_networkx_graph(filename)
      graph = to_siset_graph(G)
      del G
      start = perf_counter()
      greedy_heuristic(graph)
      end = perf_counter()
      with open(self._h('results.csv'), 'at') as file:
        file.write('{},{},{}\n'.format(
          filename, graph.packing_size(), end - start))
      del graph


  def run_experiment(self):
    with open(self._h('results.csv'), 'wt') as file:
      file.write('Grafo,Heuristica,Tiempo\n')
    for i in range(11, 18, 2):
      n = 2**i
      for j in range(1, self._num_graphs+1):
        if j < 10: j = f'0{j}'
        filename = self._h(f'{self._graph_name}_{n}_{j}.gml')
        G = load_networkx_graph(filename)
        graph = to_siset_graph(G)
        del G
        start = perf_counter()
        greedy_heuristic(graph)
        end = perf_counter()
        with open(self._h('results.csv'), 'at') as file:
          file.write('{},{},{}\n'.format(
            filename, graph.packing_size(), end-start))
