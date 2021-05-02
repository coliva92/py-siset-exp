from argparse import ArgumentParser
from .cactus import SerialCactusScripts
from .watts import WattsStrogatz4NeighborsScripts, \
  WattsStrogatz8NeighborsScripts



_SCRIPT_CONTAINERS = {
  'cactus': SerialCactusScripts,
  'watts4': WattsStrogatz4NeighborsScripts,
  'watts8': WattsStrogatz8NeighborsScripts
}




def _main(args):
  scripts = _SCRIPT_CONTAINERS[args.graph](1)
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
