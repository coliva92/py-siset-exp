from experiments import IScriptsContainer
from networkx.generators.duplication import duplication_divergence_graph




class DuplicationDivergenceGraphScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'divergente', num_graphs)
    self._params = { 'p': 0.33 }
  

  def _generate_graph(self, n):
    return duplication_divergence_graph(n, self._params['p'])
  