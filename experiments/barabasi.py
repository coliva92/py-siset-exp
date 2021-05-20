from experiments import IScriptsContainer
from networkx.generators.random_graphs import barabasi_albert_graph




class BarabasiAlbertGraphScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'barabasi', num_graphs)
    self._params = { 'm': 3 }
  

  def _generate_graph(self, n):
    return barabasi_albert_graph(n, self._params['m'])
