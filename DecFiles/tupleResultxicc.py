from Configurables import (
    DaVinci,
    EventSelector,
    PrintMCTree,
    MCDecayTreeTuple
)
from DecayTreeTuple.Configuration import *

"""Configure the variables below with:
decay: Decay you want to inspect, using 'newer' LoKi decay descriptor syntax,
decay_heads: Particles you'd like to see the decay tree of,
datafile: Where the file created by the Gauss generation phase is, and
year: What year the MC is simulating.
"""

# https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/LoKiNewDecayFinders
decay = "[Xi_cc+ => ^(Xi_cc++ => ^(Lambda_c+ => ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+) ^pi- ]CC"
decay_heads = ["Xi_cc+", "Xi_cc~-"]
datafile = "Gauss-26167053-100ev-20230302.xgen"
year = 2016
# For a quick and dirty check, you don't need to edit anything below here.
##########################################################################

# Create an MC DTT containing any candidates matching the decay descriptor
mctuple = MCDecayTreeTuple("MCDecayTreeTuple")
mctuple.Decay = decay
mctuple.ToolList = [
    "MCTupleToolHierarchy",
    "LoKi::Hybrid::MCTupleTool/LoKi_Photos"
]
# Add a 'number of photons' branch
mctuple.addTupleTool("MCTupleToolKinematic").Verbose = True
mctuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_Photos").Variables = {
    "nPhotos": "MCNINTREE(('gamma' == MCABSID))",
    "M" : "MCM"
}

# Print the decay tree for any particle in decay_heads
printMC = PrintMCTree()
printMC.ParticleNames = decay_heads

# Name of the .xgen file produced by Gauss
EventSelector().Input = ["DATAFILE='{0}' TYP='POOL_ROOTTREE' Opt='READ'".format(datafile)]

# Configure DaVinci
DaVinci().TupleFile = "DVntupleXicc_26167053.root"
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().DataType = str(year)
DaVinci().UserAlgorithms = [printMC, mctuple]

from Gaudi.Configuration import appendPostConfigAction 
def doIt():
    """
    specific post-config action for (x)GEN-files
    """
    extension = "xgen"
    ext = extension.upper()
    from Configurables import DataOnDemandSvc
    dod = DataOnDemandSvc ()
    from copy import deepcopy
    algs = deepcopy ( dod.AlgMap )
    bad = set()
    for key in algs :
        if 0 <= key.find ( 'Rec' ) : bad.add ( key )
        elif 0 <= key.find ( 'Raw' ) : bad.add ( key )
        elif 0 <= key.find ( 'DAQ' ) : bad.add ( key )
        elif 0 <= key.find ( 'Trigger' ) : bad.add ( key )
        elif 0 <= key.find ( 'Phys' ) : bad.add ( key )
        elif 0 <= key.find ( 'Prev/' ) : bad.add ( key )
        elif 0 <= key.find ( 'Next/' ) : bad.add ( key )
        elif 0 <= key.find ( '/MC/' ) and 'GEN' == ext : bad.add ( key )
        
    for b in bad :
        del algs[b]
            
    dod.AlgMap = algs
    
    from Configurables import EventClockSvc, CondDB
    EventClockSvc ( EventTimeDecoder = "FakeEventTime" )
    CondDB ( IgnoreHeartBeat = True )
    
appendPostConfigAction( doIt )
