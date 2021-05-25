from networkx.algorithms.components.connected import is_connected
from experiments import IScriptsContainer
from networkx.generators.random_graphs import erdos_renyi_graph
from siset.converters import to_siset_graph, to_networkx_graph
import networkx as nx
from os import mkdir
from os.path import isdir




class GilbertGraphScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'gilbert', num_graphs)
    self._param = {
      '2048': 0.003125,
      '8192': 0.00078125,
      '32768': 0.0001953125,
      '131072': 0.0001953125
    }
  

  def _generate_graph(self, n):
    return erdos_renyi_graph(n, self._param[f'{n}'])
