import sys

import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import DaVinci

def nodes(evt, root='/Event'):
    """List all nodes in `evt` starting from `node`."""
    node_list = [root]
    for leaf in evt.leaves(evt[root]):
        node_list += nodes(evt, leaf.identifier())
    return node_list

dv = DaVinci()
dv.DataType = '2016'
dv.Simulation = True

# Retrieve file path to open as the last command line argument
inputFiles = [sys.argv[-1]]
IOHelper('ROOT').inputFiles(inputFiles)

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

appMgr.run(1)
