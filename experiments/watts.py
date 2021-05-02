from experiments import IScriptsContainer
from networkx.generators.random_graphs import connected_watts_strogatz_graph




class WattsStrogatz4NeighborsScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'watts4', num_graphs)
    self._params = { 'k': 4, 'p': 0.5 }


  def _generate_graph(self, n):
    return connected_watts_strogatz_graph(
      n, self._params['k'], self._params['p'])




class WattsStrogatz8NeighborsScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'watts8', num_graphs)
    self._params = { 'k': 8, 'p': 0.5 }
  

  def _generate_graph(self, n):
    return connected_watts_strogatz_graph(
      n, self._params['k'], self._params['p'])
