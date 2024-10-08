#!/bin/env python
import os.path as path
import sys
from importlib import util as ilu, machinery as ilm

def main():
	spec = ilm.PathFinder().find_spec("bt", [path.dirname(path.dirname(path.realpath(__file__)))])
	bt = ilu.module_from_spec(spec)
	bt.MAIN = 1
	sys.modules[bt.__name__] = bt
	spec.loader.exec_module(bt)

if __name__ == "__main__": main()
