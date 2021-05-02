from experiments import IScriptsContainer
import networkx as nx
from siset.file import load_networkx_graph
from siset.heuristics import greedy_heuristic
from siset.cactus import serial_cactus
from siset.converters import to_siset_graph
from random import randint, uniform
from time import perf_counter




class SerialCactusScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'cactus_lineal', num_graphs)
  

  def _path_graph(self, G, curr_idx, next_idx, path_size):
    last_idx = next_idx + path_size
    while next_idx < last_idx:
      G.add_edge(curr_idx, next_idx)
      curr_idx = next_idx
      next_idx += 1
    return curr_idx, next_idx


  def _generate_graph(self, n, _):
    G = nx.Graph()
    G.add_node(0)
    n -= 1
    section_sizes = []
    i = n
    while i >= 30:
      size = randint(10, 30)
      section_sizes.append(size)
      i -= size
    section_sizes.append(i)
    j = randint(0, len(section_sizes)-1)
    section_sizes[len(section_sizes)-1] = section_sizes[j]
    section_sizes[j] = i
    curr_idx, next_idx = 0, 1
    for size in section_sizes:
      if uniform(0.0, 1.0) <= 0.5:
        print(f'{n} path')
        curr_idx, next_idx = self._path_graph(G, curr_idx, next_idx, size)
      else:
        x, y = self._path_graph(G, curr_idx, next_idx, size)
        G.add_edge(curr_idx, x)
        if (x - next_idx < 0): print(next_idx, x)
        curr_idx = randint(next_idx, x)
        next_idx = y
        print(f'{size} cycle {curr_idx}')
    return G
  

  def run_experiment(self):
    with open(self._h('results.csv'), 'wt') as file:
      file.write('Grafo,Algoritmo,Tiempo,Heuristica,Tiempo\n')
    for i in range(11, 18, 2):
      n = 2**i
      for j in range(1, self._num_graphs+1):
        if j < 10: j = f'0{j}'
        filename = self._h(f'{self._graph_name}_{n}_{j}.gml')
        G = load_networkx_graph(filename)
        graph = to_siset_graph(G)
        del G
        start = perf_counter()
        serial_cactus(graph)
        end = perf_counter()
        algo_runtime = end - start
        algo_solution = graph.packing_size()
        start = perf_counter()
        greedy_heuristic(graph)
        end = perf_counter()
        heur_runtime = end - start
        heur_solution = graph.packing_size()
        with open(self._h('results.csv'), 'at') as file:
          file.write('{},{},{},{},{}\n'.format(
            filename, algo_solution, algo_runtime, heur_solution, 
            heur_runtime))
