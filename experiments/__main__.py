from argparse import ArgumentParser
from .cactus import SerialCactusScripts
from .watts import WattsStrogatz4NeighborsScripts, \
  WattsStrogatz8NeighborsScripts
from .geometric import GeometricRandomGraphScripts
from .connected import RandomConnectedGraphScripts
from .divergent import DuplicationDivergenceGraphScripts
from .outerplanar import OuterplanarScripts
from .barabasi import BarabasiAlbertGraphScripts



_SCRIPT_CONTAINERS = {
  'cactus': SerialCactusScripts,
  'watts4': WattsStrogatz4NeighborsScripts,
  'watts8': WattsStrogatz8NeighborsScripts,
  'geometrico': GeometricRandomGraphScripts,
  'conectado': RandomConnectedGraphScripts,
  'divergente': DuplicationDivergenceGraphScripts,
  'outerplanar': OuterplanarScripts,
  'barabasi': BarabasiAlbertGraphScripts
}




def _main(args):
  scripts = _SCRIPT_CONTAINERS[args.graph]()
  if args.action == 'create': scripts.create_batch()
  elif args.action == 'metrics': scripts.compute_metrics()
  elif args.action == 'diameter': scripts.compute_diameter()
  elif args.action == 'packing': scripts.compute_packing()
  elif args.action == 'experiment': scripts.run_experiment()


def _get_args():
  parser = ArgumentParser(prog='exp')
  parser.add_argument('graph')
  parser.add_argument('action')
  return parser.parse_args()




if __name__ == '__main__':
  args = _get_args()
  _main(args)
