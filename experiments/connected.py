from experiments import IScriptsContainer
from random import randint, uniform
from networkx import from_prufer_sequence




class RandomConnectedGraphScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'conectado', num_graphs)
    self._params = { 'd': 3 }
  

  def _generate_graph(self, n):
    sequence = []
    for _ in range(n - 2): sequence.append(randint(0, n - 2))
    G = from_prufer_sequence(sequence)
    del sequence
    m = self._edge_count_from_avg_degree(n, self._params['d'])
    max_num_edges = n * (n - 1) * 0.5
    probability = (m - G.size()) / (max_num_edges - G.size())
    for i in range(n):
      for j in range(i + 1, n):
        if (not G.has_edge(i, j) and uniform(0.0, 1.0) <= probability):
          G.add_edge(i, j)
    return G


  def _edge_count_from_avg_degree(self, n, d):
    max_num_edges = n * (n - 1) * 0.5
    portion = 2 * d / (n - 1)
    return max_num_edges * portion
