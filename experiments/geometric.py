from experiments import IScriptsContainer
from networkx.generators.geometric import random_geometric_graph
from networkx import is_connected




class GeometricRandomGraphScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'geometrico', num_graphs)
    self._params = { 
      '2048': 0.05,
      '8192': 0.025,
      '32768': 0.0125,
      '131072': 0.00625
    }

  
  def _generate_graph(self, n):
    G = None
    con = False
    while not con:
      if G is not None: del G
      G = random_geometric_graph(n, self._params[f'{n}'])
      con = is_connected(G)
    return G
