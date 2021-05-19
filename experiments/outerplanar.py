from experiments import IScriptsContainer
from siset.file import load_networkx_graph
from siset.converters import to_siset_graph
from siset.heuristics import greedy_heuristic
from time import perf_counter




class OuterplanarScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'outerplanar', num_graphs)
  

  def run_experiment(self):
    with open(self._h('results.csv'), 'wt') as file:
      file.write('Grafo,Heuristica,Tiempo\n')
    for i in range(11, 18, 2):
      n = 2**i
      for j in range(1, self._num_graphs+1):
        if j < 10: j = f'0{j}'
        filename = \
          self._h(f'{self._graph_name}{n}/{self._graph_name}_{n}_{j}.gml')
        G = load_networkx_graph(filename)
        graph = to_siset_graph(G)
        del G
        start = perf_counter()
        greedy_heuristic(graph)
        end = perf_counter()
        with open(self._h('results.csv'), 'at') as file:
          file.write('{},{},{}\n'.format(
            filename, graph.packing_size(), end-start))
