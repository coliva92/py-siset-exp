from experiments import IScriptsContainer
from networkx.generators.random_graphs import connected_watts_strogatz_graph




class WattsStrogatzScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'watts', num_graphs)
    self._params = [ 4, 8 ]


  def _generate_graph(self, n, params):
    return connected_watts_strogatz_graph(n, params['k'], params['p'])


  def create_batch(self, _=None):
    for k in self._params:
      self._graph_name = f'watts{k}'
      IScriptsContainer.create_batch(self, { 'k': k, 'p': 0.5 })
