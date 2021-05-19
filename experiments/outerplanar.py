from experiments import IScriptsContainer




class OuterplanarScripts(IScriptsContainer):

  def __init__(self, num_graphs=30):
    IScriptsContainer.__init__(self, 'outerplanar', num_graphs)
  